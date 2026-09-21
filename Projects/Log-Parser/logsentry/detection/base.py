"""
Abstract base for detection rules. Rules receive a stream of
NormalizedEvents (already enriched) and decide when to fire an Alert.

Two styles supported:
  - Stateless rules: evaluate one event in isolation (e.g. "status==denied on firewall")
  - Stateful rules: need a window of events (e.g. brute force = N failures in T seconds)
    These maintain their own internal state via `evaluate`.
"""

from abc import ABC, abstractmethod
from typing import Optional
from logsentry.core.schema import NormalizedEvent, Alert


class BaseRule(ABC):

    name: str = "base_rule"
    severity: str = "medium"

    @abstractmethod
    def evaluate(self, event: NormalizedEvent) -> Optional[Alert]:
        """
        Called once per incoming event. Return an Alert if this event
        (combined with any internal state the rule keeps) triggers a
        detection. Return None otherwise.
        """
        raise NotImplementedError

    def reset(self) -> None:
        """Optional: clear internal state (used in tests / long-running resets)."""
        pass