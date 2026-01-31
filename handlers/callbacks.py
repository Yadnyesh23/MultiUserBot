from pyrogram import filters
from pyrogram.types import CallbackQuery
from app import app
from config.db import update_user_status
from utils.admin import is_owner

@app.on_callback_query()
async def callback_handler(client, callback: CallbackQuery):
    user_id = callback.from_user.id

    if not is_owner(user_id):
        await callback.answer("❌ Unauthorized", show_alert=True)
        return

    action, target_id = callback.data.split(":")
    target_id = int(target_id)

    if action == "approve":
        await update_user_status(target_id, "approved")
        await callback.message.edit_text("✅ User approved.")

    elif action == "reject":
        await update_user_status(target_id, "rejected")
        await callback.message.edit_text("❌ User rejected.")