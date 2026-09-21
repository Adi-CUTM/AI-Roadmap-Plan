"""
Timestamp parsing helpers. Log sources use wildly different formats —
centralizing this avoids every parser writing its own datetime logic.
"""

from datetime import datetime, timezone
from dateutil import parser as dateutil_parser
from dateutil.tz import tzlocal


def parse_timestamp(raw: str, assume_utc: bool = False) -> datetime:
    """
    Best-effort parse of a timestamp string into a timezone-aware datetime.
    Falls back to dateutil's fuzzy parser for odd formats (syslog's lack
    of year, for example).
    """
    try:
        dt = dateutil_parser.parse(raw, fuzzy=True)
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Could not parse timestamp: '{raw}'") from e

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc if assume_utc else tzlocal())

    return dt.astimezone(timezone.utc)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_epoch(dt: datetime) -> float:
    return dt.timestamp()