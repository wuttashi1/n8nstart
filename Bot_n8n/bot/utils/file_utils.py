from __future__ import annotations

from datetime import datetime
from pathlib import Path


def ensure_directories(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def build_unique_filename(user_id: int, original_extension: str | None, prefix: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    extension = (original_extension or "").lower()
    if extension and not extension.startswith("."):
        extension = f".{extension}"
    return f"{prefix}_{user_id}_{timestamp}{extension}"
