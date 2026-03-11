from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatMembersFilter
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error
from Yumeko.database.chatrank_db import (
    add_message,
    get_top_users,
    get_group_total,
    get_top_groups
)
from Yumeko.database.chatrank_db import (
    get_user_today,
    get_user_week,
    get_user_total,
    get_group_total
)
async def pattern_hit(value: int, start: int, step: int):
    if value < start:
        return False
    return (value - start) % step == 0
    
# Message counter
@app.on_message(filters.group & ~filters.service & ~filters.command(["ranking","groupstats","chatranks"], prefixes=config.COMMAND_PREFIXES))
async def chatrank_message_counter(client, message):

    if not message.from_user:
        return

    user = message.from_user

    await add_message(
        message.chat.id,
        user.id,
        user.first_name,
        user.username
    )

    await check_achievements(client, message)
    
    
# Leaderboard builder
async def build_leaderboard(chat_id, mode="total"):

    users = await get_top_users(chat_id, mode)

    titles = {
        "total": "🏆 **Group Leaderboard • Overall**",
        "today": "🏆 **Group Leaderboard • Today**",
        "week": "🏆 **Group Leaderboard • Weekly**"
    }

    text = f"{titles.get(mode,'🏆 Group Leaderboard')}\n\n"

    rank = 1

    for u in users:

        name = u["name"]
        username = u["username"]
        msgs = u["messages"]

        if username:
            user_text = f"[{name}](https://t.me/{username})"
        else:
            user_text = name

        text += f"{rank}. {user_text} ⋟ [ ✉️ {msgs:,} messages ]\n"

        rank += 1

    total_msgs = await get_group_total(chat_id)

    text += f"\n✉️ Total messages: {total_msgs:,}"

    return text


# Ranking command
@app.on_message(filters.command("ranking", prefixes=config.COMMAND_PREFIXES) & filters.group)
@error
@save
async def ranking(client, message):

    chat_id = message.chat.id

    text = await build_leaderboard(chat_id, "total")

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Overall", callback_data=f"rank_total_{chat_id}"),
                InlineKeyboardButton("Today", callback_data=f"rank_today_{chat_id}"),
                InlineKeyboardButton("Weekly", callback_data=f"rank_week_{chat_id}")
            ],
            [
                InlineKeyboardButton("➕ Add Me To Your Group", url="https://t.me/YumekkoRoBot?startgroup=true")
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )


# Ranking buttons
@app.on_callback_query(filters.regex("^rank_"))
async def rank_buttons(client, query: CallbackQuery):

    data = query.data.split("_")

    mode = data[1]
    chat_id = int(data[2])

    text = await build_leaderboard(chat_id, mode)

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Overall", callback_data=f"rank_total_{chat_id}"),
                InlineKeyboardButton("Today", callback_data=f"rank_today_{chat_id}"),
                InlineKeyboardButton("Weekly", callback_data=f"rank_week_{chat_id}")
            ],
            [
                InlineKeyboardButton("➕ Add Me To Your Group", url="https://t.me/YumekkoRoBot?startgroup=true")
            ]
        ]
    )

    await query.message.edit_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )

    await query.answer()

@app.on_message(filters.command("groupstats", prefixes=config.COMMAND_PREFIXES) & filters.group)
@error
@save
async def groupstats(client, message):

    chat = message.chat

    members = await client.get_chat_members_count(chat.id)
    msgs = await get_group_total(chat.id)

    groups_total = await get_top_groups("total")
    groups_today = await get_top_groups("today")
    groups_week = await get_top_groups("week")

    overall_rank = "N/A"
    today_rank = "N/A"
    week_rank = "N/A"

    for i, g in enumerate(groups_total, start=1):
        if g["chat_id"] == chat.id:
            overall_rank = i
            break

    for i, g in enumerate(groups_today, start=1):
        if g["chat_id"] == chat.id:
            today_rank = i
            break

    for i, g in enumerate(groups_week, start=1):
        if g["chat_id"] == chat.id:
            week_rank = i
            break

    text = (
        "**📊 Group Statistics**\n\n"
        f"Name ⋟ {chat.title}\n"
        f"Chat ID ⋟ `{chat.id}`\n"
        f"Members ⋟ {members:,}\n"
        f"Total Messages ⋟ {msgs:,}\n"
        f"Chat Type ⋟ {chat.type}\n\n"
        f"🏆 Group Rank\n"
        f"Overall ⋟ #{overall_rank}\n"
        f"Today ⋟ #{today_rank}\n"
        f"Weekly ⋟ #{week_rank}"
    )

    await message.reply_text(
        text,
        disable_web_page_preview=True
    )

# Global chat ranks

@app.on_message(filters.command("chatranks", prefixes=config.COMMAND_PREFIXES) & filters.private)
@error
@save
async def chatranks(client, message):

    groups = await get_top_groups()

    text = "🏆 **Top Groups By Activity**\n\n"

    rank = 1

    for g in groups:

        chat_id = g["chat_id"]
        msgs = g["messages"]

        try:
            chat = await client.get_chat(chat_id)
            name = chat.title
        except:
            name = "Unknown Chat"

        text += f"{rank}. {name} ⋟ [ ✉️ {msgs:,} messages ]\n"

        rank += 1

    await message.reply_text(text)


async def check_achievements(client, message):

    user = message.from_user
    chat = message.chat

    daily = await get_user_today(chat.id, user.id)
    weekly = await get_user_week(chat.id, user.id)
    user_total = await get_user_total(chat.id, user.id)
    group_total = await get_group_total(chat.id)

    # Daily achievement
    if daily != 0 and daily % 500 == 0:
        await message.reply_text(
            f"**Daily Achievement** ⋟ [{user.first_name}](tg://user?id={user.id}) reached [ {daily:,} messages today ]",
            disable_web_page_preview=True
        )

    # Weekly achievement
    if weekly != 0 and weekly % 2500 == 0:
        await message.reply_text(
            f"**Weekly Achievement** ⋟ [{user.first_name}](tg://user?id={user.id}) reached [ {weekly:,} messages this week ]",
            disable_web_page_preview=True
        )

    # User total achievement
    if user_total != 0 and user_total % 4000 == 0:
        await message.reply_text(
            f"**Overall Achievement** ⋟ [{user.first_name}](tg://user?id={user.id}) reached [ {user_total:,} total messages ]",
            disable_web_page_preview=True
        )

    # Group achievement
    if group_total != 0 and group_total % 4000 == 0:
        await message.reply_text(
            f"**Group Achievement** ⋟ {chat.title} reached [ {group_total:,} total messages ]",
            disable_web_page_preview=True
        )

__module__ = "𝖢𝗁𝖺𝗍 𝖱𝖺𝗇𝗄𝗌"

__help__ = """
𝖳𝗋𝖺𝖼𝗄 𝗀𝗋𝗈𝗎𝗉 𝖺𝖼𝗍𝗂𝗏𝗂𝗍𝗒 𝖺𝗇𝖽 𝗎𝗌𝖾𝗋 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗅𝖾𝖺𝖽𝖾𝗋𝖻𝗈𝖺𝗋𝖽𝗌.

**Commands**

• `/ranking`
Shows the group leaderboard.

• `/groupstats`
Shows detailed group statistics.

• `/chatranks`
Shows top active groups.
"""
