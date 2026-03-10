from pyrogram import Client
from pyrogram.errors import ChatAdminRequired
from Yumeko.database import warnings_collection
from Yumeko import app

DEFAULT_WARNS = 3  # default warn limit


async def set_warn_limit(chat_id: int, limit: int):
    """
    Set warn limit for a specific chat.
    """
    await warnings_collection.update_one(
        {"chat_id": chat_id, "type": "settings"},
        {"$set": {"warn_limit": limit}},
        upsert=True
    )


async def get_warn_limit(chat_id: int):
    """
    Get warn limit for a specific chat.
    """
    data = await warnings_collection.find_one({"chat_id": chat_id, "type": "settings"})
    if not data:
        return DEFAULT_WARNS
    return data.get("warn_limit", DEFAULT_WARNS)


async def add_warn(chat_id: int, user_id: int, reason: str, client: Client):
    """
    Add a warning to a user and check ban condition.
    """

    warn_limit = await get_warn_limit(chat_id)

    warn_data = await warnings_collection.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )

    if not warn_data:
        warn_data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "warn_count": 0,
            "reasons": []
        }

    warn_data["warn_count"] += 1
    warn_data["reasons"].append(reason)

    await warnings_collection.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": warn_data},
        upsert=True
    )

    if warn_data["warn_count"] >= warn_limit:
        await ban_user(chat_id, user_id, client)

    return warn_data["warn_count"]


async def ban_user(chat_id: int, user_id: int, client: Client):
    """
    Ban user and clear warns.
    """
    try:
        await app.ban_chat_member(chat_id, user_id)
        await clear_warns(chat_id, user_id)

    except ChatAdminRequired:
        return
    except Exception:
        return


async def remove_warn(chat_id: int, user_id: int):
    """
    Remove one warn from user.
    """
    warn_data = await warnings_collection.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )

    if not warn_data or warn_data["warn_count"] == 0:
        return 0

    warn_data["warn_count"] -= 1

    if warn_data["reasons"]:
        warn_data["reasons"].pop()

    await warnings_collection.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": warn_data}
    )

    return warn_data["warn_count"]


async def get_warn_count(chat_id: int, user_id: int):
    """
    Get user warn count.
    """
    warn_data = await warnings_collection.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )

    if not warn_data:
        return 0

    return warn_data["warn_count"]


async def get_warn_reasons(chat_id: int, user_id: int):
    """
    Get warn reasons.
    """
    warn_data = await warnings_collection.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )

    if not warn_data:
        return []

    return warn_data["reasons"]


async def clear_warns(chat_id: int, user_id: int):
    """
    Clear all warns of a user.
    """
    await warnings_collection.delete_one(
        {"chat_id": chat_id, "user_id": user_id}
    )
