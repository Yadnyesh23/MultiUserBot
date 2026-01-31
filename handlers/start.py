from app import app
from pyrogram import filters
from config.env import OWNER_ID
from config.db import get_user, create_user, get_all_users

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user = message.from_user
    
    db_user = await get_user(user.id)
    
    if db_user is None:
        new_user = await create_user(user)
        
        if new_user['role'] == 'owner':
            await message.reply_text( "👑 Welcome Owner!\n\nYou have full access to this bot.")
        else:
            await message.reply_text("👋 Welcome!\n\nYour access request has been sent to the owner.")
    
    role = db_user.get("role")
    status = db_user.get("status")
    if role == "owner":
        await message.reply_text("👑 Welcome back, Owner!")
    elif status == "approved":
        await message.reply_text("✅ You are approved!\nUse /login to continue.")
    else:
        await message.reply_text("⏳ Your access request is still pending approval.")

   