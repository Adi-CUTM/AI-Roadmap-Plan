"""
Abstract base for all ingestion sources (file tail, batch read, syslog, etc.)
Each ingestor is a generator that yields raw log lines as strings.
Parsing, enrichment, detection all happen downstream in the pipeline —
ingestors know NOTHING about log formats.
"""

from abc import ABC, abstractmethod
from typing import Iterator


class BaseIngestor(ABC):

    name: str = "base_ingestor"

    @abstractmethod
    def stream(self) -> Iterator[str]:
        """
        Yield raw log lines one at a time. For real-time sources this
        blocks/waits for new lines (like `tail -f`); for batch sources
        it reads until EOF and stops.
        """
        raise NotImplementedError

    def close(self) -> None:
        """Optional cleanup hook (close file handles, sockets, etc.)."""
        pass