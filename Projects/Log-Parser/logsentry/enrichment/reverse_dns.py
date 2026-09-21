"""
Reverse DNS enrichment — resolves source_ip to a hostname where possible.
Uses a short timeout and in-memory cache since DNS lookups are slow and
the same IPs repeat constantly in real log traffic.
"""

import socket
from typing import Optional

from logsentry.enrichment.base import BaseEnricher
from logsentry.core.schema import NormalizedEvent
from logsentry.utils.logger import get_logger

logger = get_logger("enrichment.reverse_dns")

socket.setdefaulttimeout(1.5)  # never let a slow DNS server stall the pipeline


class ReverseDNSEnricher(BaseEnricher):
    name = "reverse_dns"

    def __init__(self, cache_size: int = 10_000):
        self._cache: dict[str, Optional[str]] = {}
        self._cache_size = cache_size

    def enrich(self, event: NormalizedEvent) -> NormalizedEvent:
        if not event.source_ip:
            return event

        ip_str = str(event.source_ip)

        if ip_str in self._cache:
            event.reverse_dns = self._cache[ip_str]
            return event

        hostname = self._resolve(ip_str)

        if len(self._cache) >= self._cache_size:
            self._cache.pop(next(iter(self._cache)))  # crude FIFO eviction
        self._cache[ip_str] = hostname

        event.reverse_dns = hostname
        return event

    def _resolve(self, ip: str) -> Optional[str]:
        try:
            return socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror, socket.timeout):
            return None
        except Exception as e:  # noqa: BLE001
            logger.debug(f"Reverse DNS failed for {ip}: {e}")
            return None