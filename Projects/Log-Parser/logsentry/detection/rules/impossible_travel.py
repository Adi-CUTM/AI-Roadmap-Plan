"""
Detects "impossible travel": same user authenticating successfully
from two geographically distant locations within a time window too
short for real travel. Requires GeoIP enrichment to have already run
(event.geo_country / geo_city must be populated).
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from logsentry.detection.base import BaseRule
from logsentry.core.schema import NormalizedEvent, Alert, Severity, EventCategory
from logsentry.utils.logger import get_logger

logger = get_logger("detection.impossible_travel")


class ImpossibleTravelRule(BaseRule):
    name = "impossible_travel"
    severity = Severity.HIGH

    def __init__(self, max_window_minutes: int = 60):
        self.max_window = timedelta(minutes=max_window_minutes)
        # user -> (timestamp, country, source_ip)
        self._last_login: dict[str, tuple[datetime, str, str]] = {}

    def evaluate(self, event: NormalizedEvent) -> Optional[Alert]:
        if event.category != EventCategory.AUTHENTICATION:
            return None
        if event.status != "success":
            return None
        if not event.user or not event.geo_country or not event.source_ip:
            return None  # can't evaluate without enrichment data

        user = event.user
        prev = self._last_login.get(user)
        self._last_login[user] = (event.timestamp, event.geo_country, str(event.source_ip))

        if not prev:
            return None

        prev_ts, prev_country, prev_ip = prev
        time_diff = event.timestamp - prev_ts

        if prev_country == event.geo_country:
            return None  # same country, not suspicious
        if time_diff > self.max_window:
            return None  # enough time to plausibly travel / VPN change coincidence

        logger.info(
            f"Impossible travel for user {user}: {prev_country} -> {event.geo_country} "
            f"in {time_diff}"
        )

        return Alert(
            alert_id=str(uuid.uuid4()),
            rule_name=self.name,
            severity=self.severity,
            title=f"Impossible travel detected for user '{user}'",
            description=(
                f"User '{user}' logged in from {prev_country} ({prev_ip}) and then "
                f"from {event.geo_country} ({event.source_ip}) "
                f"within {time_diff.total_seconds():.0f} seconds"
            ),
            triggered_at=event.timestamp,
            matched_events=[event],
            tags=["authentication", "impossible_travel"],
            extra={
                "user": user,
                "from_country": prev_country,
                "to_country": event.geo_country,
                "time_diff_seconds": time_diff.total_seconds(),
            },
        )

    def reset(self) -> None:
        self._last_login.clear()