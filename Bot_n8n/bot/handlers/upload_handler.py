import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from bot.services.file_service import UnsupportedMediaError, download_media_file
from bot.services.state_service import upload_state_service

logger = logging.getLogger(__name__)


async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.message or not update.effective_user:
        return

    upload_state_service.mark_waiting(update.effective_user.id)
    await update.message.reply_text("Please send an audio or video file now.")


async def media_upload_receiver(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    if not upload_state_service.is_waiting(user_id):
        return

    try:
        saved_path = await download_media_file(update.message, context, user_id)
    except UnsupportedMediaError as exc:
        await update.message.reply_text(str(exc))
        return
    except Exception:
        logger.exception("Unexpected upload error for user %s", user_id)
        await update.message.reply_text("Failed to download your file. Please try again.")
        return

    upload_state_service.set_last_uploaded_path(user_id, saved_path)
    upload_state_service.clear_waiting(user_id)
    await update.message.reply_text(f"File received and saved at: {saved_path}")


def register(application) -> None:
    application.add_handler(CommandHandler("upload", upload_command))
    application.add_handler(
        MessageHandler(filters.AUDIO | filters.VIDEO | filters.VIDEO_NOTE, media_upload_receiver)
    )
