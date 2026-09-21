"""
Batch file reader for historical log analysis — reads a file
start-to-finish and stops. No tailing, no checkpointing needed.
"""

from pathlib import Path
from typing import Iterator

from logsentry.ingestion.base import BaseIngestor
from logsentry.core.exceptions import SourceNotFoundError
from logsentry.utils.logger import get_logger

logger = get_logger("ingestion.batch_reader")


class BatchReader(BaseIngestor):
    name = "batch_reader"

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise SourceNotFoundError(f"Log file not found: {file_path}")

    def stream(self) -> Iterator[str]:
        logger.info(f"Batch reading {self.file_path}")
        with open(self.file_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.rstrip("\n")
                if line:
                    yield line