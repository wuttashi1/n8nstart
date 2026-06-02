from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class UserUploadState:
    waiting_for_file: bool = False
    last_uploaded_path: Path | None = None


class UploadStateService:
    def __init__(self) -> None:
        self._state: dict[int, UserUploadState] = {}

    def mark_waiting(self, user_id: int) -> None:
        state = self._state.setdefault(user_id, UserUploadState())
        state.waiting_for_file = True

    def clear_waiting(self, user_id: int) -> None:
        state = self._state.setdefault(user_id, UserUploadState())
        state.waiting_for_file = False

    def is_waiting(self, user_id: int) -> bool:
        state = self._state.get(user_id)
        return bool(state and state.waiting_for_file)

    def set_last_uploaded_path(self, user_id: int, path: Path) -> None:
        state = self._state.setdefault(user_id, UserUploadState())
        state.last_uploaded_path = path

    def get_last_uploaded_path(self, user_id: int) -> Path | None:
        state = self._state.get(user_id)
        if not state:
            return None
        return state.last_uploaded_path


upload_state_service = UploadStateService()
