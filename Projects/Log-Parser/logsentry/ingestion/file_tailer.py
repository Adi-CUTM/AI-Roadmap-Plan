"""
Real-time file tailing ingestor — the `tail -f` equivalent, with
checkpoint support so restarts resume from the last read byte offset
instead of reprocessing the whole file.
"""

import time
from pathlib import Path
from typing import Iterator, Optional

from logsentry.ingestion.base import BaseIngestor
from logsentry.core.checkpoint import CheckpointStore
from logsentry.core.exceptions import SourceNotFoundError
from logsentry.utils.logger import get_logger

logger = get_logger("ingestion.file_tailer")


class FileTailer(BaseIngestor):
    """
    Tails a single log file. Handles:
      - resuming from checkpoint offset
      - log rotation (inode change or file truncation)
      - graceful wait when no new data is available
    """

    name = "file_tailer"

    def __init__(
        self,
        file_path: str,
        checkpoint_store: Optional[CheckpointStore] = None,
        poll_interval: float = 0.5,
        from_beginning: bool = False,
    ):
        self.file_path = Path(file_path)
        self.checkpoint_store = checkpoint_store
        self.poll_interval = poll_interval
        self.from_beginning = from_beginning
        self._fh = None
        self._current_inode: Optional[int] = None

        if not self.file_path.exists():
            raise SourceNotFoundError(f"Log file not found: {file_path}")

    def _open(self) -> None:
        self._fh = open(self.file_path, "r", encoding="utf-8", errors="replace")
        self._current_inode = self.file_path.stat().st_ino

        if self.checkpoint_store and not self.from_beginning:
            offset = self.checkpoint_store.get_offset(str(self.file_path))
            self._fh.seek(offset)
        elif not self.from_beginning:
            self._fh.seek(0, 2)  # seek to EOF — only stream new lines

    def _rotated(self) -> bool:
        """Detect log rotation via inode change or file shrink."""
        try:
            stat = self.file_path.stat()
        except FileNotFoundError:
            return True  # file removed mid-tail, treat as rotation
        if stat.st_ino != self._current_inode:
            return True
        if self._fh and stat.st_size < self._fh.tell():
            return True  # truncated
        return False

    def stream(self) -> Iterator[str]:
        self._open()
        logger.info(f"Tailing {self.file_path} (poll={self.poll_interval}s)")

        try:
            while True:
                line = self._fh.readline()

                if line:
                    if self.checkpoint_store:
                        self.checkpoint_store.set_offset(
                            str(self.file_path), self._fh.tell()
                        )
                    yield line.rstrip("\n")
                else:
                    if self._rotated():
                        logger.info(f"Rotation detected for {self.file_path}, reopening")
                        self._fh.close()
                        self._open()
                        continue
                    time.sleep(self.poll_interval)
        finally:
            self.close()

    def close(self) -> None:
        if self._fh:
            self._fh.close()
            self._fh = None