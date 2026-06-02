import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from bot.services.n8n_client import N8nClientError, send_upload_event
from bot.services.telegram_downloader import FileDownloadError, download_user_media
from bot.services.user_state import user_state_store

logger = logging.getLogger(__name__)


async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.message or not update.effective_user:
        return
    user_state_store.mark_waiting(update.effective_user.id)
    await update.message.reply_text("Send audio or video file now.")


async def on_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    if not user_state_store.is_waiting(user_id):
        return

    try:
        file_path, file_type = await download_user_media(update.message, context, user_id=user_id)
        user_state_store.set_last_upload(user_id, file_path, file_type)
        user_state_store.clear_waiting(user_id)

        payload = {
            "user_id": str(user_id),
            "file_path": str(file_path),
            "file_type": file_type,
            "file_name": file_path.name,
        }
        n8n_response = send_upload_event(payload)
        logger.info("Upload event sent to n8n: user_id=%s file=%s", user_id, file_path)

        await update.message.reply_text(
            f"File uploaded: {file_path.name}\n"
            f"Stored in: {file_path}\n"
            f"n8n response: {n8n_response}"
        )
    except FileDownloadError as exc:
        await update.message.reply_text(str(exc))
    except N8nClientError:
        await update.message.reply_text("File saved, but failed to notify n8n. Please retry /render later.")
    except Exception:
        logger.exception("Unexpected upload flow error: user_id=%s", user_id)
        await update.message.reply_text("Unexpected upload error. Please try again.")


def register(application) -> None:
    application.add_handler(CommandHandler("upload", upload_command))
    application.add_handler(MessageHandler(filters.AUDIO | filters.VIDEO | filters.VIDEO_NOTE, on_media))
