from pyrogram import Client, filters
from pyrogram.types import Message
from config.db import users_col
from config.env import BOT_TOKEN

active_clients = {}  # store active clients for each user

@Client.on_message(filters.command("login") & filters.private)
async def auto_login(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Check if user already logged in
    if user_id in active_clients:
        await message.reply("✅ You are already logged in!")
        return
    
    # Fetch session string from MongoDB
    user_data = users_col.find_one({"user_id": user_id})
    
    if not user_data or "session_string" not in user_data:
        await message.reply(
            "❌ You are not registered. Contact the bot owner to get access."
        )
        return
    
    session_string = user_data["session_string"]
    
    # Create Pyrogram client for this user
    user_client = Client(
        name=f"user_{user_id}",
        session_string=session_string
    )
    
    # Start client
    await user_client.start()
    active_clients[user_id] = user_client
    
    await message.reply("✅ You are now logged in! Enjoy the bot features.")