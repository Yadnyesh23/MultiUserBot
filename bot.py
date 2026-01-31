from pyrogram import Client
from app import app

from handlers import start

if __name__  == '__main__':
    print("Bot started ...")
    app.run()