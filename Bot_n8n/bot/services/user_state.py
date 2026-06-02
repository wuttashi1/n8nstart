from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class UserState:
    waiting_for_upload: bool = False
    last_uploaded_file: Path | None = None
    last_file_type: str | None = None


class UserStateStore:
    def __init__(self) -> None:
        self._store: dict[int, UserState] = {}

    def mark_waiting(self, user_id: int) -> None:
        state = self._store.setdefault(user_id, UserState())
        state.waiting_for_upload = True

    def clear_waiting(self, user_id: int) -> None:
        state = self._store.setdefault(user_id, UserState())
        state.waiting_for_upload = False

    def is_waiting(self, user_id: int) -> bool:
        state = self._store.get(user_id)
        return bool(state and state.waiting_for_upload)

    def set_last_upload(self, user_id: int, file_path: Path, file_type: str) -> None:
        state = self._store.setdefault(user_id, UserState())
        state.last_uploaded_file = file_path
        state.last_file_type = file_type

    def get_last_upload(self, user_id: int) -> tuple[Path | None, str | None]:
        state = self._store.get(user_id)
        if not state:
            return None, None
        return state.last_uploaded_file, state.last_file_type


user_state_store = UserStateStore()
