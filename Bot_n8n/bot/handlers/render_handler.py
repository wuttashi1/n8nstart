from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.services.render_service import simulate_video_processing, trigger_render
from bot.services.state_service import upload_state_service


async def render_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.message or not update.effective_user:
        return

    user = update.effective_user
    file_path = upload_state_service.get_last_uploaded_path(user.id)

    if not file_path:
        await update.message.reply_text("No uploaded file found. Use /upload first.")
        return

    await update.message.reply_text("Triggering render workflow...")
    ok, message = trigger_render(file_path=file_path, user_id=user.id, username=user.username)
    if not ok:
        await update.message.reply_text(f"Render trigger failed. {message}")
        return

    await update.message.reply_text("Render request accepted. Processing video...")
    result = await simulate_video_processing()
    await update.message.reply_text(result)


def register(application) -> None:
    application.add_handler(CommandHandler("render", render_command))
