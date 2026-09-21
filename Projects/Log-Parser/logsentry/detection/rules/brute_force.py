"""
Detects brute-force login attempts: N failed logins from the same
source IP within a sliding time window.
"""

import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Optional

from logsentry.detection.base import BaseRule
from logsentry.core.schema import NormalizedEvent, Alert, Severity, EventCategory
from logsentry.utils.logger import get_logger

logger = get_logger("detection.brute_force")


class BruteForceRule(BaseRule):
    name = "brute_force_login"
    severity = Severity.HIGH

    def __init__(self, threshold: int = 5, window_seconds: int = 60):
        self.threshold = threshold
        self.window = timedelta(seconds=window_seconds)
        # per-source-ip sliding window of failure timestamps
        self._failures: dict[str, deque] = defaultdict(deque)
        # avoid re-firing every single event once threshold is crossed
        self._already_alerted: dict[str, datetime] = {}

    def evaluate(self, event: NormalizedEvent) -> Optional[Alert]:
        if event.category != EventCategory.AUTHENTICATION:
            return None
        if event.status != "failure":
            return None
        if not event.source_ip:
            return None

        ip = str(event.source_ip)
        window_start = event.timestamp - self.window

        dq = self._failures[ip]
        dq.append(event.timestamp)

        # drop entries outside the window
        while dq and dq[0] < window_start:
            dq.popleft()

        if len(dq) < self.threshold:
            return None

        # cooldown: don't re-alert on every event once already firing
        last_alert = self._already_alerted.get(ip)
        if last_alert and (event.timestamp - last_alert) < self.window:
            return None

        self._already_alerted[ip] = event.timestamp
        logger.info(f"Brute force detected from {ip}: {len(dq)} failures in {self.window}")

        return Alert(
            alert_id=str(uuid.uuid4()),
            rule_name=self.name,
            severity=self.severity,
            title=f"Brute force login attempt from {ip}",
            description=(
                f"{len(dq)} failed login attempts from {ip} "
                f"within {self.window.total_seconds():.0f} seconds "
                f"(threshold: {self.threshold})"
            ),
            triggered_at=event.timestamp,
            matched_events=[event],
            tags=["authentication", "brute_force"],
            extra={"source_ip": ip, "failure_count": len(dq)},
        )

    def reset(self) -> None:
        self._failures.clear()
        self._already_alerted.clear()