from pyrogram import filters
from pyrogram.errors import FloodWait, UserAlreadyParticipant
import asyncio

from app import app
from utils.permissions import is_logged_in
from utils.session import get_user_client

@app.on_message(filters.command("join") & filters.private)
async def join_groups(client, message):
    user_id = message.from_user.id

    if not await is_logged_in(user_id):
        await message.reply_text("🔐 Please /login first.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage:\n/join link1 link2 link3")
        return

    links = message.command[1:]
    user_client = await get_user_client(user_id)

    if not user_client:
        await message.reply_text("❌ Session not found.")
        return

    success, failed = 0, 0

    await user_client.start()

    for link in links:
        try:
            await user_client.join_chat(link)
            success += 1
            await asyncio.sleep(2)

        except UserAlreadyParticipant:
            success += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            failed += 1

    await user_client.stop()

    await message.reply_text(
        f"✅ Joined: {success}\n❌ Failed: {failed}"
    )