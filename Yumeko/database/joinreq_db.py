from Yumeko.database import db

joinreq_collection = db["join_requests"]


async def enable_joinreq(chat_id: int):
    await joinreq_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": True}},
        upsert=True,
    )


async def disable_joinreq(chat_id: int):
    await joinreq_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": False}},
        upsert=True,
    )


async def is_joinreq_enabled(chat_id: int) -> bool:
    data = await joinreq_collection.find_one({"chat_id": chat_id})
    if not data:
        return False
    return data.get("enabled", False)
