"""
Abstract base for enrichment steps. Each enricher takes a NormalizedEvent
and returns it with additional fields populated (geo, ASN, threat score, etc).
Enrichers must NEVER raise uncaught — the pipeline already wraps calls in
try/except, but enrichers should fail soft internally too where possible.
"""

from abc import ABC, abstractmethod
from logsentry.core.schema import NormalizedEvent


class BaseEnricher(ABC):

    name: str = "base_enricher"

    @abstractmethod
    def enrich(self, event: NormalizedEvent) -> NormalizedEvent:
        """Mutate and return the event with additional context filled in."""
        raise NotImplementedError