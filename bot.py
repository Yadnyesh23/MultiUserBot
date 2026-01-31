from pyrogram import Client
from app import app

from handlers import start , approval , login , admin , broadcast , callbacks , join

if __name__  == '__main__':
    print("Bot started ...")
    app.run()