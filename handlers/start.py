from app import app
from pyrogram import filters
from config.env import OWNER_ID

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id

    if user_id == OWNER_ID:
        await message.reply_text(
            "👑 Welcome Owner!\n\n"
            "You have full access to this bot."
        )
    else:
        await message.reply_text(
            "👋 Welcome!\n\n"
            "Your access request is pending approval.\n"
            "Please wait for the owner to approve you."
        )