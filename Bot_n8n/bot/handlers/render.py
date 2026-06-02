import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.services.n8n_client import N8nClientError, send_render_event
from bot.services.user_state import user_state_store

logger = logging.getLogger(__name__)


async def render_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    last_file, _ = user_state_store.get_last_upload(user_id)
    if not last_file:
        await update.message.reply_text("No uploaded file found. Use /upload first.")
        return

    payload = {
        "user_id": str(user_id),
        "last_uploaded_file": str(last_file),
        "action": "render_video",
    }

    try:
        result = send_render_event(payload)
        logger.info("Render requested: user_id=%s file=%s", user_id, last_file)
        await update.message.reply_text(f"Render request sent.\nn8n response: {result}")
    except N8nClientError as exc:
        await update.message.reply_text(f"Render request failed: {exc}")
    except Exception:
        logger.exception("Unexpected render error: user_id=%s", user_id)
        await update.message.reply_text("Unexpected error while sending render request.")


def register(application) -> None:
    application.add_handler(CommandHandler("render", render_command))
