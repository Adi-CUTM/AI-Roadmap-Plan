"""
Appends alerts as newline-delimited JSON (NDJSON) to a file — the
standard format for downstream ingestion into a SIEM (Elastic,
Splunk, etc.) via a log shipper like Filebeat.
"""

import json
from pathlib import Path
from threading import Lock

from logsentry.output.base import BaseOutput
from logsentry.core.schema import Alert
from logsentry.core.exceptions import OutputError


class JsonFileOutput(BaseOutput):
    name = "json_file"

    def __init__(self, output_path: str = "data/alerts.ndjson"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def send_alert(self, alert: Alert) -> None:
        try:
            line = alert.model_dump_json()
            with self._lock:
                with open(self.output_path, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
        except Exception as e:
            raise OutputError(f"Failed to write alert to {self.output_path}: {e}") from e