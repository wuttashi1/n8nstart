from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import requests

from bot.config import settings

logger = logging.getLogger(__name__)


def trigger_render(file_path: Path, user_id: int, username: str | None) -> tuple[bool, str]:
    payload = {
        "file_path": str(file_path),
        "user": {
            "id": user_id,
            "username": username,
        },
    }
    try:
        response = requests.post(settings.n8n_webhook_url, json=payload, timeout=20)
        response.raise_for_status()
        return True, "Render webhook triggered successfully."
    except requests.RequestException as exc:
        logger.exception("Failed to trigger render webhook for user %s", user_id)
        return False, f"Webhook error: {exc}"


async def simulate_video_processing() -> str:
    await asyncio.sleep(7)
    return "Video ready."
