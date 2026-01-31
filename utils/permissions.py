from config.db import get_user, get_session
from config.env import OWNER_ID

async def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


async def is_approved(user_id: int) -> bool:
    user = await get_user(user_id)
    return bool(user and user.get("status") == "approved")


async def is_logged_in(user_id: int) -> bool:
    session = await get_session(user_id)
    return bool(session)