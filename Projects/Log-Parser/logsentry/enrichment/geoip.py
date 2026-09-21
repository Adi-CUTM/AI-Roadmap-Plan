"""
GeoIP enrichment using MaxMind's GeoLite2 City database.
Populates geo_country, geo_city on events that have a source_ip.

Requires a GeoLite2-City.mmdb file — see scripts/setup_geoip_db.sh
or download manually from MaxMind (free account required):
https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
"""

from pathlib import Path
from typing import Optional

import geoip2.database
import geoip2.errors

from logsentry.enrichment.base import BaseEnricher
from logsentry.core.schema import NormalizedEvent
from logsentry.utils.logger import get_logger

logger = get_logger("enrichment.geoip")

# RFC1918 / private ranges — skip lookups for these, they'll never resolve
_PRIVATE_PREFIXES = ("10.", "192.168.", "127.", "169.254.")
_PRIVATE_172_RANGE = range(16, 32)  # 172.16.0.0 - 172.31.255.255


def _is_private_ip(ip: str) -> bool:
    if ip.startswith(_PRIVATE_PREFIXES):
        return True
    if ip.startswith("172."):
        try:
            second_octet = int(ip.split(".")[1])
            return second_octet in _PRIVATE_172_RANGE
        except (IndexError, ValueError):
            return False
    return False


class GeoIPEnricher(BaseEnricher):
    name = "geoip"

    def __init__(self, db_path: str = "data/GeoLite2-City.mmdb"):
        self.db_path = Path(db_path)
        self._reader: Optional[geoip2.database.Reader] = None

        if self.db_path.exists():
            self._reader = geoip2.database.Reader(str(self.db_path))
            logger.info(f"GeoIP database loaded from {self.db_path}")
        else:
            logger.warning(
                f"GeoIP database not found at {self.db_path} — "
                "geo enrichment will be skipped. Run scripts/setup_geoip_db.sh"
            )

    def enrich(self, event: NormalizedEvent) -> NormalizedEvent:
        if not self._reader or not event.source_ip:
            return event

        ip_str = str(event.source_ip)
        if _is_private_ip(ip_str):
            return event

        try:
            response = self._reader.city(ip_str)
            event.geo_country = response.country.iso_code
            event.geo_city = response.city.name
        except geoip2.errors.AddressNotFoundError:
            pass  # IP not in database — not an error, just no data
        except Exception as e:  # noqa: BLE001
            logger.debug(f"GeoIP lookup failed for {ip_str}: {e}")

        return event

    def close(self) -> None:
        if self._reader:
            self._reader.close()