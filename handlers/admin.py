from pyrogram import filters
from app import app
from utils.admin import is_owner
from config.db import get_all_users

@app.on_message(filters.command("users") & filters.private)
async def users_handler(client, message):
    if not is_owner(message.from_user.id):
        return

    users = await get_all_users()

    text = "👥 Users List\n\n"
    for user in users:
        text += (
            f"🆔 {user['user_id']} | "
            f"Role: {user['role']} | "
            f"Status: {user['status']}\n"
        )

    await message.reply_text(text)
    
@app.on_message(filters.command("stats") & filters.private)
async def stats_handler(client, message):
    if not is_owner(message.from_user.id):
        return

    users = await get_all_users()

    total = len(users)
    approved = len([u for u in users if u["status"] == "approved"])
    pending = len([u for u in users if u["status"] == "pending"])

    await message.reply_text(
        f"📊 Bot Stats\n\n"
        f"👥 Total Users: {total}\n"
        f"✅ Approved: {approved}\n"
        f"⏳ Pending: {pending}"
    )

@app.on_message(filters.command("ban") & filters.private)
async def ban_handler(client, message):
    if not is_owner(message.from_user.id):
        return

    try:
        target_id = int(message.text.split()[1])
    except:
        await message.reply_text("Usage: /ban <user_id>")
        return

    from config.db import update_user_status
    await update_user_status(target_id, "banned")

    await message.reply_text("🚫 User banned.")