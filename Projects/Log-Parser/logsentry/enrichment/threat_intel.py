"""
Threat intel enrichment — checks source IPs against:
  1. A local blocklist file (always available, no API key needed)
  2. AbuseIPDB API (optional — requires ABUSEIPDB_API_KEY env var)

Populates event.threat_score (0-100) and event.is_known_bad.
Designed to degrade gracefully: if no API key is set, only the
local blocklist is used — the tool still works.
"""

import os
import time
from pathlib import Path
from typing import Optional

import requests

from logsentry.enrichment.base import BaseEnricher
from logsentry.core.schema import NormalizedEvent
from logsentry.utils.logger import get_logger

logger = get_logger("enrichment.threat_intel")


class ThreatIntelEnricher(BaseEnricher):
    name = "threat_intel"

    def __init__(
        self,
        blocklist_path: str = "config/blocklist.txt",
        api_key: Optional[str] = None,
        cache_ttl_seconds: int = 3600,
    ):
        self.blocklist_path = Path(blocklist_path)
        self.api_key = api_key or os.getenv("ABUSEIPDB_API_KEY")
        self.cache_ttl = cache_ttl_seconds

        self._blocklist: set[str] = self._load_blocklist()
        self._api_cache: dict[str, tuple[float, float]] = {}  # ip -> (score, expiry)

        if not self.api_key:
            logger.warning(
                "No ABUSEIPDB_API_KEY set — threat intel will only use local blocklist"
            )

    def _load_blocklist(self) -> set[str]:
        if not self.blocklist_path.exists():
            logger.info(f"No local blocklist found at {self.blocklist_path}, skipping")
            return set()
        with open(self.blocklist_path) as f:
            ips = {line.strip() for line in f if line.strip() and not line.startswith("#")}
        logger.info(f"Loaded {len(ips)} IPs from local blocklist")
        return ips

    def enrich(self, event: NormalizedEvent) -> NormalizedEvent:
        if not event.source_ip:
            return event

        ip_str = str(event.source_ip)

        # 1. Local blocklist — instant, always checked
        if ip_str in self._blocklist:
            event.is_known_bad = True
            event.threat_score = 100.0
            return event

        # 2. AbuseIPDB — only if API key present
        if self.api_key:
            score = self._check_abuseipdb(ip_str)
            if score is not None:
                event.threat_score = score
                event.is_known_bad = score >= 75.0

        return event

    def _check_abuseipdb(self, ip: str) -> Optional[float]:
        # Cache check
        cached = self._api_cache.get(ip)
        if cached and cached[1] > time.time():
            return cached[0]

        try:
            response = requests.get(
                "https://api.abuseipdb.com/api/v2/check",
                headers={"Key": self.api_key, "Accept": "application/json"},
                params={"ipAddress": ip, "maxAgeInDays": 90},
                timeout=3,
            )
            response.raise_for_status()
            score = float(response.json()["data"]["abuseConfidenceScore"])
            self._api_cache[ip] = (score, time.time() + self.cache_ttl)
            return score
        except requests.RequestException as e:
            logger.debug(f"AbuseIPDB lookup failed for {ip}: {e}")
            return None
        except (KeyError, ValueError) as e:
            logger.debug(f"AbuseIPDB response parsing failed for {ip}: {e}")
            return None