from __future__ import annotations

import logging
from pathlib import Path

from telegram import Audio, Message, Video, VideoNote
from telegram.ext import ContextTypes

from bot.config import settings
from bot.utils.file_manager import ensure_directories, unique_filename

logger = logging.getLogger(__name__)


class FileDownloadError(Exception):
    pass


def _extract_media(message: Message) -> tuple[str, str, str]:
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

    raise FileDownloadError("Please send audio or video file.")


async def download_user_media(
    message: Message,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
) -> tuple[Path, str]:
    ensure_directories(settings.music_input_dir, settings.video_input_dir)

    try:
        file_id, extension, file_type = _extract_media(message)
        target_dir = settings.music_input_dir if file_type == "music" else settings.video_input_dir
        filename = unique_filename(user_id=user_id, extension=extension, prefix=file_type)
        destination = target_dir / filename

        tg_file = await context.bot.get_file(file_id)
        await tg_file.download_to_drive(custom_path=str(destination))

        logger.info("Upload saved: user_id=%s type=%s path=%s", user_id, file_type, destination)
        return destination, file_type
    except FileDownloadError:
        raise
    except Exception as exc:
        logger.exception("Failed to download media for user_id=%s", user_id)
        raise FileDownloadError("Could not download your file. Please try again.") from exc
