from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def ensure_directories(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def unique_filename(user_id: int, extension: str, prefix: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    normalized_ext = extension.lower()
    if normalized_ext and not normalized_ext.startswith("."):
        normalized_ext = f".{normalized_ext}"
    return f"{prefix}_{user_id}_{timestamp}{normalized_ext}"
