from __future__ import annotations

import logging
from typing import Any

import requests

from bot.config import settings

logger = logging.getLogger(__name__)


class N8nClientError(Exception):
    pass


def _post(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{settings.n8n_webhook_url}/{endpoint.lstrip('/')}"
    try:
        response = requests.post(url, json=payload, timeout=25)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("n8n request failed: %s", endpoint)
        raise N8nClientError(f"Failed to call n8n endpoint '{endpoint}': {exc}") from exc

    if not response.content:
        return {"ok": True}

    try:
        data = response.json()
        return data if isinstance(data, dict) else {"result": data}
    except ValueError:
        return {"raw_response": response.text}


def send_upload_event(payload: dict[str, Any]) -> dict[str, Any]:
    return _post("upload", payload)


def send_render_event(payload: dict[str, Any]) -> dict[str, Any]:
    return _post("render", payload)


def fetch_status(payload: dict[str, Any]) -> dict[str, Any]:
    return _post("status", payload)
