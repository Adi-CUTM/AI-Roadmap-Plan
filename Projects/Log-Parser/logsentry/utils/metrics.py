"""
Lightweight in-process metrics tracker for LogSentry's own health.
Thread-safe counters exposed via a snapshot dict — can later be
scraped by a /metrics endpoint (Prometheus) without changing callers.
"""

import threading
import time
from dataclasses import dataclass, field


@dataclass
class MetricsSnapshot:
    events_ingested: int
    events_parsed: int
    parse_failures: int
    events_enriched: int
    alerts_fired: int
    output_failures: int
    uptime_seconds: float
    events_per_second: float


class Metrics:
    """Singleton-style metrics collector. Import `metrics` instance directly."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._start_time = time.monotonic()
        self._counters = {
            "events_ingested": 0,
            "events_parsed": 0,
            "parse_failures": 0,
            "events_enriched": 0,
            "alerts_fired": 0,
            "output_failures": 0,
        }

    def incr(self, key: str, amount: int = 1) -> None:
        with self._lock:
            if key not in self._counters:
                self._counters[key] = 0
            self._counters[key] += amount

    def snapshot(self) -> MetricsSnapshot:
        with self._lock:
            uptime = max(time.monotonic() - self._start_time, 1e-6)
            eps = self._counters["events_ingested"] / uptime
            return MetricsSnapshot(
                events_ingested=self._counters["events_ingested"],
                events_parsed=self._counters["events_parsed"],
                parse_failures=self._counters["parse_failures"],
                events_enriched=self._counters["events_enriched"],
                alerts_fired=self._counters["alerts_fired"],
                output_failures=self._counters["output_failures"],
                uptime_seconds=uptime,
                events_per_second=round(eps, 2),
            )

    def reset(self) -> None:
        with self._lock:
            for k in self._counters:
                self._counters[k] = 0
            self._start_time = time.monotonic()


# Single shared instance — import this everywhere
metrics = Metrics()