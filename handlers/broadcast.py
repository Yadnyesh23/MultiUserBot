from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, ChatWriteForbidden
import asyncio

from app import app
from utils.permissions import is_logged_in
from utils.session import get_user_client

@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client, message):
    user_id = message.from_user.id

    if not await is_logged_in(user_id):
        await message.reply_text("🔐 Please /login first.")
        return

    if not message.reply_to_message:
        await message.reply_text(
            "📢 Reply to a message with /broadcast to send it to all groups."
        )
        return

    user_client = await get_user_client(user_id)
    if not user_client:
        await message.reply_text("❌ Session not found.")
        return

    status = await message.reply_text("🚀 Broadcast started...")

    success, failed = 0, 0
    await user_client.start()

    async for dialog in user_client.get_dialogs():
        chat = dialog.chat

        if chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
            continue

        try:
            await user_client.copy_message(
                chat_id=chat.id,
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.id
            )
            success += 1
            await asyncio.sleep(2)

        except ChatWriteForbidden:
            failed += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception as e:
            failed += 1
            print(f"Failed for {chat.id} → {e}")

    await user_client.stop()

    await status.edit_text(
        f"✅ Broadcast completed!\n\n"
        f"📨 Sent: {success}\n"
        f"❌ Failed: {failed}"
    )