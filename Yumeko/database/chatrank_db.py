from Yumeko.database import db
from datetime import datetime

chatrank_collection = db.ChatRanks
groupstats_collection = db.GroupStats


async def add_message(chat_id: int, user_id: int, name: str, username: str | None):

    today = datetime.utcnow().strftime("%Y-%m-%d")
    week = datetime.utcnow().strftime("%Y-%W")

    await chatrank_collection.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {
            "$inc": {
                "total": 1,
                f"daily.{today}": 1,
                f"weekly.{week}": 1
            },
            "$set": {
                "name": name,
                "username": username
            }
        },
        upsert=True
    )

    await groupstats_collection.update_one(
        {"chat_id": chat_id},
        {"$inc": {"messages": 1}},
        upsert=True
    )

async def get_top_users(chat_id: int, mode: str = "total", limit: int = 10):

    today = datetime.utcnow().strftime("%Y-%m-%d")
    week = datetime.utcnow().strftime("%Y-%W")

    if mode == "today":
        key = f"daily.{today}"
    elif mode == "week":
        key = f"weekly.{week}"
    else:
        key = "total"

    cursor = chatrank_collection.find({"chat_id": chat_id}).sort(key, -1).limit(limit)

    users = []
    async for u in cursor:

        if mode == "today":
            msgs = u.get("daily", {}).get(today, 0)
        elif mode == "week":
            msgs = u.get("weekly", {}).get(week, 0)
        else:
            msgs = u.get("total", 0)

        users.append(
            {
                "user_id": u["user_id"],
                "name": u.get("name"),
                "username": u.get("username"),
                "messages": msgs
            }
        )

    return users

async def get_group_total(chat_id: int):

    data = await groupstats_collection.find_one({"chat_id": chat_id})

    if not data:
        return 0

    return data.get("messages", 0)

async def get_top_groups(limit: int = 10):

    cursor = groupstats_collection.find().sort("messages", -1).limit(limit)

    groups = []

    async for g in cursor:
        groups.append(
            {
                "chat_id": g["chat_id"],
                "messages": g.get("messages", 0)
            }
        )

    return groups

async def get_group_rank(chat_id: int):

    groups = groupstats_collection.find().sort("messages", -1)

    rank = 1

    async for g in groups:

        if g["chat_id"] == chat_id:
            return rank

        rank += 1

    return None
