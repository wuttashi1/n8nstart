from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    n8n_webhook_url: str
    download_path: Path
    input_dir: Path
    music_input_dir: Path
    video_input_dir: Path
    log_dir: Path
    log_file: Path


def _require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_PATH = Path(os.getenv("DOWNLOAD_PATH", str(BASE_DIR / "input"))).expanduser()
INPUT_DIR = DOWNLOAD_PATH
LOG_DIR = BASE_DIR / "logs"

settings = Settings(
    telegram_bot_token=_require_env("TELEGRAM_BOT_TOKEN"),
    n8n_webhook_url=_require_env("N8N_WEBHOOK_URL").rstrip("/"),
    download_path=DOWNLOAD_PATH,
    input_dir=INPUT_DIR,
    music_input_dir=INPUT_DIR / "music",
    video_input_dir=INPUT_DIR / "video",
    log_dir=LOG_DIR,
    log_file=LOG_DIR / "bot.log",
)
