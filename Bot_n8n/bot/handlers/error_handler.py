import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled exception while processing update %s", update, exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("An internal error occurred. Please try again later.")
