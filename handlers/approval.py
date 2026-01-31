from app import app
from pyrogram import filters
from config.env import OWNER_ID
from config.db import get_all_users, get_user , create_user, approve_user, reject_user

@app.on_callback_query(filters.regex('^(approve|reject):'))
async def approve_handler(client, callback_query):
    if callback_query.from_user.id != OWNER_ID:
        await callback_query.answer( "❌ You are not authorized.",
            show_alert=True)
        return
    
    action , user_id = callback_query.data.split(":")
    user_id = int(user_id)
    
    user = await get_user(user_id)
    
    if not user:
        await callback_query.answer("⚠️ User not found.", show_alert=True)
        return
    
    if action == "approve":
        await approve_user(user_id)
        await callback_query.edit_message_text(
            f"✅ User `{user_id}` approved."
        )
        await client.send_message(
            user_id,
            "🎉 Your access has been approved!\nUse /start again."
        )

    elif action == "reject":
        await reject_user(user_id)
        await callback_query.edit_message_text(
            f"❌ User `{user_id}` rejected."
        )