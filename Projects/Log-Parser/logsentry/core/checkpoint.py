"""
Tracks byte offsets per log file so the pipeline can resume exactly
where it left off after a restart/crash, instead of reprocessing
the whole file or losing lines.
"""

import json
from pathlib import Path
from threading import Lock
from logsentry.utils.logger import get_logger

logger = get_logger("core.checkpoint")


class CheckpointStore:
    def __init__(self, checkpoint_file: str = "data/checkpoints.json"):
        self.checkpoint_file = Path(checkpoint_file)
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._state: dict[str, int] = self._load()

    def _load(self) -> dict[str, int]:
        if self.checkpoint_file.exists():
            try:
                return json.loads(self.checkpoint_file.read_text())
            except json.JSONDecodeError:
                logger.warning("Checkpoint file corrupted — starting fresh")
                return {}
        return {}

    def get_offset(self, source_path: str) -> int:
        with self._lock:
            return self._state.get(source_path, 0)

    def set_offset(self, source_path: str, offset: int) -> None:
        with self._lock:
            self._state[source_path] = offset
            self._flush()

    def _flush(self) -> None:
        # Atomic write: write to temp file then rename, avoids corruption
        # if the process is killed mid-write.
        tmp_path = self.checkpoint_file.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(self._state, indent=2))
        tmp_path.replace(self.checkpoint_file)