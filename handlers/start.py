from app import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.env import OWNER_ID
from config.db import get_user, create_user

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user

    db_user = await get_user(user.id)

    
    if db_user is None:
        new_user = await create_user(user)

        
        if new_user["role"] == "owner":
            await message.reply_text(
                "👑 Welcome Owner!\n\nYou have full access to this bot."
            )
            return

        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user.id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{user.id}")
            ]
        ])

        await client.send_message(
            OWNER_ID,
            text=(
                "🔔 New User Request\n\n"
                f"👤 User ID: `{user.id}`\n"
                f"👤 Username: @{user.username}"
            ),
            reply_markup=keyboard
        )

        await message.reply_text(
            "👋 Welcome!\n\nYour access request has been sent to the owner."
        )
        return 

    role = db_user.get("role")
    status = db_user.get("status")

    if role == "owner":
        await message.reply_text("👑 Welcome back, Owner!")
    elif status == "approved":
        await message.reply_text("✅ You are approved!\nUse /login to continue.")
    else:
        await message.reply_text("⏳ Your access request is still pending approval.")