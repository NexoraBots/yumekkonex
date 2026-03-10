from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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


async def build_leaderboard(chat_id, mode="total"):

    users = await get_top_users(chat_id, mode)

    text = "🏆 **𝖦𝗋𝗈𝗎𝗉 𝖫𝖾𝖺𝖽𝖾𝗋𝖻𝗈𝖺𝗋𝖽**\n\n"

    rank = 1

    for u in users:

        name = u["name"]
        username = u["username"]
        msgs = u["messages"]

        if username:
            user_text = f"[{name}](https://t.me/{username})"
        else:
            user_text = name

        medals = ["🥇","🥈","🥉"]

        if rank <= 3:
            badge = medals[rank-1]
        else:
            badge = "🔹"

        text += f"{badge} **{rank}.** {user_text}\n"
        text += f"   ✉️ {msgs:,} messages\n\n"

        rank += 1

    total_msgs = await get_group_total(chat_id)

    text += f"━━━━━━━━━━━━━━\n"
    text += f"📊 **Total Messages:** {total_msgs:,}"

    return text


@app.on_message(filters.command("ranking", prefixes=config.COMMAND_PREFIXES) & filters.group)
@error
@save
async def ranking(client, message):

    text = await build_leaderboard(message.chat.id, "total")

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Overall", callback_data=f"rank_total_{message.chat.id}"),
                InlineKeyboardButton("Today", callback_data=f"rank_today_{message.chat.id}"),
                InlineKeyboardButton("Weekly", callback_data=f"rank_week_{message.chat.id}")
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )


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

    admins = await client.get_chat_members(chat.id, filter="administrators")

    admin_count = 0

    async for _ in admins:
        admin_count += 1

    try:
        creator = (await client.get_chat_member(chat.id, chat.id)).user
        creator_name = creator.first_name
    except:
        creator_name = "Unknown"

    text = (
        "📊 **𝖦𝗋𝗈𝗎𝗉 𝖲𝗍𝖺𝗍𝗂𝗌𝗍𝗂𝖼𝗌**\n\n"
        f"🏷 **Name:** {chat.title}\n"
        f"🆔 **Chat ID:** `{chat.id}`\n"
        f"👥 **Members:** {members:,}\n"
        f"👮 **Admins:** {admin_count}\n"
        f"✉️ **Total Messages:** {msgs:,}\n"
        f"📅 **Chat Type:** {chat.type}\n"
    )

    await message.reply_text(text)


@app.on_message(filters.command("chatranks", prefixes=config.COMMAND_PREFIXES) & filters.private)
@error
@save
async def chatranks(client, message):

    groups = await get_top_groups()

    text = "🏆 **𝖳𝗈𝗉 𝖦𝗋𝗈𝗎𝗉𝗌 𝖻𝗒 𝖠𝖼𝗍𝗂𝗏𝗂𝗍𝗒**\n\n"

    rank = 1

    for g in groups:

        chat_id = g["chat_id"]
        msgs = g["messages"]

        try:
            chat = await client.get_chat(chat_id)
            name = chat.title
        except:
            name = "Unknown Chat"

        medals = ["🥇","🥈","🥉"]

        if rank <= 3:
            badge = medals[rank-1]
        else:
            badge = "🔹"

        text += f"{badge} **{rank}. {name}**\n"
        text += f"`{chat_id}`\n"
        text += f"✉️ {msgs:,} messages\n\n"

        rank += 1

    await message.reply_text(text)


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
