from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.errors import ChatAdminRequired

from Yumeko import app
from Yumeko.database import warn_db
from Yumeko.decorator.chatadmin import can_restrict_members
from Yumeko.decorator.errors import error
from Yumeko.decorator.save import save
from config import config

RESTRICT = None


@app.on_message(filters.command("warn", prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def warn_user(client: Client, message: Message):

    try:

        if len(message.command) < 2 and not message.reply_to_message:
            return await message.reply(
                "<b>Usage:</b> Reply or /warn user reason",
                parse_mode=ParseMode.HTML
            )

        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided."

        target_user = await resolve_user(client, message)

        if not target_user:
            return await message.reply(
                "<b>Error:</b> Unable to identify the user.",
                parse_mode=ParseMode.HTML
            )

        x = await app.get_chat_member(message.chat.id, target_user.id)

        if x.status == ChatMemberStatus.OWNER:
            return await message.reply("You can't warn the owner.")

        if x.status == ChatMemberStatus.ADMINISTRATOR:
            return await message.reply("User is admin.")

        warn_count = await warn_db.add_warn(message.chat.id, target_user.id, reason, client)

        MAX_WARNS = await warn_db.get_warn_limit(message.chat.id)

        user_mention = target_user.mention

        if warn_count >= MAX_WARNS:
            await message.reply(
                f"**User Banned:** {user_mention}\n"
                f"**Reason:** {reason}\n"
                f"**Warn Limit Reached:** {MAX_WARNS}"
            )
            return

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("-1", callback_data=f"warn_decrease_{target_user.id}"),
                InlineKeyboardButton("+1", callback_data=f"warn_increase_{target_user.id}")
            ],
            [
                InlineKeyboardButton("Clear Warns", callback_data=f"warn_delete_{target_user.id}")
            ],
            [
                InlineKeyboardButton("🗑", callback_data="delete")
            ]
        ])

        await message.reply(
            f"**Warning Issued:** {user_mention}\n"
            f"**Reason:** {reason}\n"
            f"**Current Warns:** {warn_count}/{MAX_WARNS}",
            reply_markup=keyboard
        )

    except ChatAdminRequired:
        await message.reply("I need admin rights.")

@app.on_message(filters.command("setwarnlimit", prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def set_warn_limit(client: Client, message: Message):

    if len(message.command) < 2:
        return await message.reply("Usage: /setwarnlimit 3")

    try:
        limit = int(message.command[1])

        await warn_db.set_warn_limit(message.chat.id, limit)

        await message.reply(
            f"Warn limit updated.\nNew limit: {limit}"
        )

    except ValueError:
        await message.reply("Invalid number.")
        
@app.on_message(filters.command("resetwarns", prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def reset_warns(client: Client, message: Message):

    target_user = await resolve_user(client, message)

    if not target_user:
        return await message.reply("User not found.")

    await warn_db.clear_warns(message.chat.id, target_user.id)

    await message.reply(
        f"All warnings reset for {target_user.mention}"
    )
    
@app.on_message(filters.command("unwarn", prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def unwarn_user(client: Client, message: Message):

    try:

        target_user = await resolve_user(client, message)

        if not target_user:
            return await message.reply("User not found.")

        warn_count = await warn_db.remove_warn(message.chat.id, target_user.id)

        if warn_count == 0:
            return await message.reply(
                f"No warnings left for {target_user.mention}"
            )

        await message.reply(
            f"Warning removed for {target_user.mention}\nRemaining: {warn_count}"
        )

    except ChatAdminRequired:
        await message.reply("Admin rights required.")


__module__ = "𝖶𝖺𝗋𝗇"


__help__ = """**𝖶𝖺𝗋𝗇𝗂𝗇𝗀 𝖲𝗒𝗌𝗍𝖾𝗆**

- **𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**

✧ `/warn <user> [reason]`
✧ `/unwarn <user>`
✧ `/setwarnlimit <number>`
✧ `/resetwarns <user>`

- **𝖣𝖾𝗍𝖺𝗂𝗅𝗌:**

✧ 𝖶𝗁𝖾𝗇 𝗐𝖺𝗋𝗇𝗌 𝗋𝖾𝖺𝖼𝗁 𝗅𝗂𝗆𝗂𝗍, 𝗎𝗌𝖾𝗋 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖻𝖺𝗇𝗇𝖾𝖽.
✧ 𝖠𝖽𝗆𝗂𝗇𝗌 𝖼𝖺𝗇 𝗂𝗇𝖼𝗋𝖾𝖺𝗌𝖾/𝖽𝖾𝖼𝗋𝖾𝖺𝗌𝖾 𝗐𝖺𝗋𝗇𝗌 𝗎𝗌𝗂𝗇𝗀 𝖻𝗎𝗍𝗍𝗈𝗇𝗌.
"""
