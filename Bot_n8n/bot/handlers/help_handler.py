from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.constants import HELP_MESSAGE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await update.message.reply_text(HELP_MESSAGE)


def register(application) -> None:
    application.add_handler(CommandHandler("help", help_command))
