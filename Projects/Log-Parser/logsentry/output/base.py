"""
Abstract base for all output sinks. An output sink takes an Alert
(or optionally a raw NormalizedEvent for full audit trails) and
delivers it somewhere — console, file, Slack, Elasticsearch, etc.
"""

from abc import ABC, abstractmethod
from logsentry.core.schema import Alert


class BaseOutput(ABC):

    name: str = "base_output"

    @abstractmethod
    def send_alert(self, alert: Alert) -> None:
        """Deliver a single alert. Must raise OutputError on failure,
        never fail silently."""
        raise NotImplementedError

    def close(self) -> None:
        """Optional cleanup (flush buffers, close connections)."""
        pass