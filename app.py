from pyrogram import Client
from config.env import API_HASH, API_ID, BOT_TOKEN

app = Client(
    "BusinessBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)