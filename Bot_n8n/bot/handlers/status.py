import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.services.n8n_client import N8nClientError, fetch_status

logger = logging.getLogger(__name__)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    payload = {"user_id": str(user_id)}

    try:
        data = fetch_status(payload)
        rendering_status = data.get("rendering_status", "unknown")
        queue_position = data.get("queue_position", "n/a")
        last_video_result = data.get("last_video_result", "n/a")

        text = (
            "Pipeline status:\n"
            f"- Rendering: {rendering_status}\n"
            f"- Queue position: {queue_position}\n"
            f"- Last video: {last_video_result}"
        )
        await update.message.reply_text(text)
    except N8nClientError as exc:
        await update.message.reply_text(f"Status request failed: {exc}")
    except Exception:
        logger.exception("Unexpected status error: user_id=%s", user_id)
        await update.message.reply_text("Unexpected error while requesting status.")


def register(application) -> None:
    application.add_handler(CommandHandler("status", status_command))
