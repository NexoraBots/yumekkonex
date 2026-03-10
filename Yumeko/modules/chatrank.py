import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error
from Yumeko.database import mongodb

db = mongodb

msgdb = db["chat_messages"]
groupdb = db["group_stats"]

@app.on_message(filters.group & filters.text & ~filters.bot)
async def message_counter(client, message):

    user = message.from_user
    chat = message.chat

    today = datetime.date.today().isoformat()
    week = datetime.date.today().isocalendar()[1]

    await msgdb.update_one(
        {"chat_id": chat.id, "user_id": user.id},
        {
            "$inc": {
                "total": 1,
                f"daily.{today}": 1,
                f"weekly.{week}": 1
            },
            "$set": {
                "name": user.first_name,
                "username": user.username
            }
        },
        upsert=True
    )

    await groupdb.update_one(
        {"chat_id": chat.id},
        {"$inc": {"messages": 1}},
        upsert=True
    )

async def get_leaderboard(chat_id, mode="total"):

    today = datetime.date.today().isoformat()
    week = datetime.date.today().isocalendar()[1]

    if mode == "today":
        key = f"daily.{today}"
    elif mode == "week":
        key = f"weekly.{week}"
    else:
        key = "total"

    users = msgdb.find({"chat_id": chat_id}).sort(key, -1).limit(10)

    text = "📈 **LEADERBOARD**\n\n"
    rank = 1

    async for user in users:

        name = user.get("name", "User")
        username = user.get("username")

        msgs = user.get("total", 0)

        if mode == "today":
            msgs = user.get("daily", {}).get(today, 0)

        if mode == "week":
            msgs = user.get("weekly", {}).get(week, 0)

        if username:
            user_text = f"[{name}](https://t.me/{username})"
        else:
            user_text = name

        text += f"{rank}. 👤 {user_text} • {msgs:,}\n"
        rank += 1

    total = await groupdb.find_one({"chat_id": chat_id})
    total_msgs = total.get("messages", 0) if total else 0

    text += f"\n✉️ **Total messages:** {total_msgs:,}"

    return text

@app.on_message(filters.command("ranking", prefixes=config.COMMAND_PREFIXES) & filters.group)
@error
@save
async def ranking(client, message):

    text = await get_leaderboard(message.chat.id, "total")

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Overall", callback_data=f"rank_total_{message.chat.id}"),
                InlineKeyboardButton("Today", callback_data=f"rank_today_{message.chat.id}"),
                InlineKeyboardButton("Weekly", callback_data=f"rank_week_{message.chat.id}")
            ]
        ]
    )

    await message.reply_text(text, reply_markup=buttons, disable_web_page_preview=True)

@app.on_callback_query(filters.regex("^rank_"))
async def rank_buttons(client, query: CallbackQuery):

    data = query.data.split("_")
    mode = data[1]
    chat_id = int(data[2])

    text = await get_leaderboard(chat_id, mode)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Overall", callback_data=f"rank_total_{chat_id}"),
                InlineKeyboardButton("Today", callback_data=f"rank_today_{chat_id}"),
                InlineKeyboardButton("Weekly", callback_data=f"rank_week_{chat_id}")
            ]
        ]
    )

    await query.message.edit_text(text, reply_markup=buttons, disable_web_page_preview=True)

@app.on_message(filters.command("groupstats", prefixes=config.COMMAND_PREFIXES) & filters.group)
@error
@save
async def groupstats(client, message):

    chat = message.chat
    members = await client.get_chat_members_count(chat.id)

    stats = await groupdb.find_one({"chat_id": chat.id})
    msgs = stats.get("messages", 0) if stats else 0

    text = (
        f"📊 **GROUP STATISTICS**\n\n"
        f"**Name:** {chat.title}\n"
        f"**Chat ID:** `{chat.id}`\n"
        f"**Members:** {members:,}\n"
        f"**Total Messages:** {msgs:,}\n"
    )

    await message.reply_text(text)

@app.on_message(filters.command("chatranks", prefixes=config.COMMAND_PREFIXES) & filters.private)
@error
@save
async def chatranks(client, message):

    groups = groupdb.find().sort("messages", -1).limit(10)

    text = "🏆 **TOP GROUPS BY MESSAGES**\n\n"
    rank = 1

    async for g in groups:

        chat_id = g["chat_id"]
        msgs = g.get("messages", 0)

        try:
            chat = await client.get_chat(chat_id)
            name = chat.title
        except:
            name = "Unknown"

        text += f"{rank}. {name}\n"
        text += f"`{chat_id}` • {msgs:,} msgs\n\n"

        rank += 1

    await message.reply_text(text)

__module__ = "𝖢𝗁𝖺𝗍 𝖱𝖺𝗇𝗄𝗌"

__help__ = """
𝖳𝗋𝖺𝖼𝗄 𝖼𝗁𝖺𝗍 𝖺𝖼𝗍𝗂𝗏𝗂𝗍𝗒 𝖺𝗇𝖽 𝗅𝖾𝖺𝖽𝖾𝗋𝖻𝗈𝖺𝗋𝖽𝗌.

**Commands:**

• /ranking  
Shows group leaderboard with buttons:
Overall • Today • Weekly

• /groupstats  
Shows detailed statistics of the group.

• /chatranks  
Shows top groups ranked by total messages.
"""
