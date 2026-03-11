from Yumeko.database import db
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

chatrank_collection = db.ChatRanks
groupstats_collection = db.GroupStats


def get_today():
    return datetime.now(IST).strftime("%Y-%m-%d")


def get_week():
    return datetime.now(IST).strftime("%Y-%W")


async def get_user_today(chat_id: int, user_id: int):

    today = get_today()

    data = await chatrank_collection.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )

    if not data:
        return 0

    return data.get("daily", {}).get(today, 0)


async def get_user_week(chat_id: int, user_id: int):

    week = get_week()

    data = await chatrank_collection.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )

    if not data:
        return 0

    return data.get("weekly", {}).get(week, 0)


async def get_user_total(chat_id: int, user_id: int):

    data = await chatrank_collection.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )

    if not data:
        return 0

    return data.get("total", 0)


async def add_message(chat_id: int, user_id: int, name: str, username: str | None):

    today = get_today()
    week = get_week()

    # Update user stats
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

    # Update group stats
    await groupstats_collection.update_one(
        {"chat_id": chat_id},
        {
            "$inc": {
                "messages": 1,
                f"daily.{today}": 1,
                f"weekly.{week}": 1
            }
        },
        upsert=True
    )

async def get_top_users(chat_id: int, mode: str = "total", limit: int = 10):

    today = get_today()
    week = get_week()

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

async def get_group_today(chat_id: int):

    today = get_today()

    data = await groupstats_collection.find_one({"chat_id": chat_id})

    if not data:
        return 0

    return data.get("daily", {}).get(today, 0)

async def get_group_week(chat_id: int):

    week = get_week()

    data = await groupstats_collection.find_one({"chat_id": chat_id})

    if not data:
        return 0

    return data.get("weekly", {}).get(week, 0)


async def get_top_groups(mode="total", limit: int = 10):

    today = get_today()
    week = get_week()

    if mode == "today":
        key = f"daily.{today}"
    elif mode == "week":
        key = f"weekly.{week}"
    else:
        key = "messages"

    cursor = groupstats_collection.find().sort(key, -1).limit(limit)

    groups = []

    async for g in cursor:

        if mode == "today":
            msgs = g.get("daily", {}).get(today, 0)
        elif mode == "week":
            msgs = g.get("weekly", {}).get(week, 0)
        else:
            msgs = g.get("messages", 0)

        groups.append(
            {
                "chat_id": g["chat_id"],
                "messages": msgs
            }
        )

    return groups

async def get_top_groups(mode: str = "total", limit: int = 10):
    today = get_today()
    week = get_week()

    key_map = {
        "today": f"daily.{today}",
        "week": f"weekly.{week}",
        "total": "messages"
    }

    key = key_map.get(mode, "messages")
    cursor = groupstats_collection.find().sort(key, -1).limit(limit)

    groups = []
    async for g in cursor:
        msgs = g.get("daily", {}).get(today, 0) if mode == "today" else \
               g.get("weekly", {}).get(week, 0) if mode == "week" else \
               g.get("messages", 0)
        groups.append({"chat_id": g["chat_id"], "messages": msgs})
    return groups
    
# Cleanup old daily data (keep last 7 days)
async def cleanup_daily():

    async for user in chatrank_collection.find():

        daily = user.get("daily", {})

        if len(daily) > 7:

            keys = sorted(daily.keys())[:-7]

            for k in keys:
                await chatrank_collection.update_one(
                    {"_id": user["_id"]},
                    {"$unset": {f"daily.{k}": ""}}
                )


# Cleanup old weekly data (keep last 4 weeks)
async def cleanup_weekly():

    async for user in chatrank_collection.find():

        weekly = user.get("weekly", {})

        if len(weekly) > 4:

            keys = sorted(weekly.keys())[:-4]

            for k in keys:
                await chatrank_collection.update_one(
                    {"_id": user["_id"]},
                    {"$unset": {f"weekly.{k}": ""}}
                )
