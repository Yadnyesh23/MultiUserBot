from motor.motor_asyncio import AsyncIOMotorClient
from config.env import MONGO_URI, DB_NAME , OWNER_ID
from datetime import datetime

#Mongo DB COnnection

mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo[DB_NAME]

users_col = db.users


#CRUD operation on user
async def get_user(user_id:int):
    return await users_col.find_one({"user_id" : user_id})

async def get_all_users():
    users = users_col.find({})
    return await users.to_list(length=None)

async def create_user(user):
    data = {
        "user_id": user.id,
        "username": user.username,
        "created_at": datetime.utcnow()
    }

    if user.id == OWNER_ID:
        data.update({
            "role": "owner",
            "status": "approved"
        })
    else:
        data.update({
            "role": "user",
            "status": "pending"
        })

    await users_col.insert_one(data)
    return data

async def update_user_status(user_id: int, status: str):
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"status": status}}
    )