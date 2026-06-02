from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.constants import WELCOME_MESSAGE


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await update.message.reply_text(WELCOME_MESSAGE)


def register(application) -> None:
    application.add_handler(CommandHandler("start", start_command))
