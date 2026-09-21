"""
Rule engine: holds all active detection rules and runs each incoming
event through every one of them. Rules are independent — one throwing
an exception should never take down the others or the pipeline.
"""

from typing import Optional
from logsentry.detection.base import BaseRule
from logsentry.core.schema import NormalizedEvent, Alert
from logsentry.core.exceptions import RuleEvaluationError
from logsentry.utils.logger import get_logger
from logsentry.utils.metrics import metrics

logger = get_logger("detection.rule_engine")


class RuleEngine:
    def __init__(self) -> None:
        self._rules: list[BaseRule] = []

    def register(self, rule: BaseRule) -> None:
        logger.info(f"Registering detection rule: {rule.name}")
        self._rules.append(rule)

    def evaluate(self, event: NormalizedEvent) -> list[Alert]:
        alerts: list[Alert] = []
        for rule in self._rules:
            try:
                result = rule.evaluate(event)
                if result:
                    alerts.append(result)
                    metrics.incr("alerts_fired")
            except Exception as e:  # noqa: BLE001 — one bad rule must not kill others
                logger.error(f"Rule '{rule.name}' failed evaluating event {event.event_id}: {e}")
        return alerts

    def reset_all(self) -> None:
        for rule in self._rules:
            rule.reset()

    @property
    def registered_names(self) -> list[str]:
        return [r.name for r in self._rules]


def bootstrap_rules(config: Optional[dict] = None) -> RuleEngine:
    """Explicit rule registration, mirrors bootstrap_parsers()."""
    from logsentry.detection.rules.brute_force import BruteForceRule
    from logsentry.detection.rules.impossible_travel import ImpossibleTravelRule

    config = config or {}
    engine = RuleEngine()

    bf_cfg = config.get("brute_force", {})
    engine.register(BruteForceRule(
        threshold=bf_cfg.get("threshold", 5),
        window_seconds=bf_cfg.get("window_seconds", 60),
    ))

    it_cfg = config.get("impossible_travel", {})
    engine.register(ImpossibleTravelRule(
        max_window_minutes=it_cfg.get("max_window_minutes", 60),
    ))

    return engine