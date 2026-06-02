from __future__ import annotations

import logging
from pathlib import Path

from telegram import Audio, Message, Video, VideoNote
from telegram.ext import ContextTypes

from bot.config import settings
from bot.utils.file_utils import build_unique_filename, ensure_directories

logger = logging.getLogger(__name__)


class UnsupportedMediaError(Exception):
    pass


def _extract_file_data(message: Message) -> tuple[str, str, str]:
    if message.audio:
        audio: Audio = message.audio
        extension = Path(audio.file_name).suffix if audio.file_name else ".mp3"
        return audio.file_id, extension, "music"

    if message.video:
        video: Video = message.video
        extension = Path(video.file_name).suffix if video.file_name else ".mp4"
        return video.file_id, extension, "video"

    if message.video_note:
        video_note: VideoNote = message.video_note
        return video_note.file_id, ".mp4", "video"

    raise UnsupportedMediaError("Only audio and video files are supported right now.")


async def download_media_file(message: Message, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> Path:
    ensure_directories(settings.music_input_dir, settings.video_input_dir)

    file_id, extension, media_type = _extract_file_data(message)
    remote_file = await context.bot.get_file(file_id)

    base_path = settings.music_input_dir if media_type == "music" else settings.video_input_dir
    filename = build_unique_filename(user_id=user_id, original_extension=extension, prefix=media_type)
    destination = base_path / filename

    await remote_file.download_to_drive(custom_path=str(destination))
    logger.info("Saved %s file for user %s at %s", media_type, user_id, destination)
    return destination
