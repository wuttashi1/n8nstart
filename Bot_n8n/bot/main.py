import asyncio

from telegram.ext import Application

from bot.config import settings
from bot.handlers import error, render, start, status, upload
from bot.utils.logger import configure_logging


async def run_bot() -> None:
    configure_logging(settings.log_file)

    application = Application.builder().token(settings.telegram_bot_token).build()
    start.register(application)
    upload.register(application)
    render.register(application)
    status.register(application)
    application.add_error_handler(error.on_error)

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    try:
        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
