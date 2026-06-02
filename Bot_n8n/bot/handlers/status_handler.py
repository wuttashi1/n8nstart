from datetime import datetime, timezone

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.message:
        return

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    text = (
        "System status (mock):\n"
        "- Bot: online\n"
        "- n8n webhook: configured\n"
        "- Render worker: standby\n"
        f"- Time: {now}"
    )
    await update.message.reply_text(text)


def register(application) -> None:
    application.add_handler(CommandHandler("status", status_command))
