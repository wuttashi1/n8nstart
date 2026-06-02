from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


START_TEXT = (
    "Welcome to AI Factory Control Bot.\n\n"
    "I can help you:\n"
    "- upload music/video files\n"
    "- trigger rendering in n8n\n"
    "- check current pipeline status\n"
    "- choose channel in future versions\n\n"
    "Commands:\n"
    "/upload - send music/video\n"
    "/render - start render workflow\n"
    "/status - check render queue/status\n"
    "/help - list commands"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await update.message.reply_text(START_TEXT)


def register(application) -> None:
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", start_command))
