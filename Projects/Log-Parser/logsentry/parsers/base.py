"""
Abstract base class every log parser must implement.
This is the plugin contract — new log sources = new file here,
zero changes to the pipeline.
"""

from abc import ABC, abstractmethod
from typing import Optional
from logsentry.core.schema import NormalizedEvent


class BaseParser(ABC):
    """
    Contract:
      - `name` uniquely identifies this parser (used as log_source value)
      - `can_parse` should be CHEAP (e.g. regex match / substring check),
        it's called on every line during auto-detection
      - `parse` does the real work and must raise ParseError on failure,
        never return None silently
    """

    name: str = "base"

    @abstractmethod
    def can_parse(self, raw_line: str) -> bool:
        """Quick check: does this line look like something this parser handles?"""
        raise NotImplementedError

    @abstractmethod
    def parse(self, raw_line: str) -> NormalizedEvent:
        """Parse a raw line into a NormalizedEvent. Raise ParseError on failure."""
        raise NotImplementedError

    def parse_safe(self, raw_line: str) -> Optional[NormalizedEvent]:
        """
        Non-raising wrapper used by the pipeline so one bad line
        doesn't kill the whole stream. Logs and swallows ParseError.
        """
        from logsentry.core.exceptions import ParseError
        from logsentry.utils.logger import get_logger

        logger = get_logger(f"parsers.{self.name}")
        try:
            return self.parse(raw_line)
        except ParseError as e:
            logger.warning(f"Parse failure in {self.name}: {e} | line={raw_line!r}")
            return None
        except Exception as e:  # noqa: BLE001 — deliberately broad, must never crash pipeline
            logger.error(f"Unexpected error in {self.name} parser: {e} | line={raw_line!r}")
            return None