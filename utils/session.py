from pyrogram import Client
from config.db import get_session
from config.env import API_ID, API_HASH

async def get_user_client(user_id: int) -> Client | None:
    session_string = await get_session(user_id)
    if not session_string:
        return None

    return Client(
        name=f"user_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
        in_memory=True
    )