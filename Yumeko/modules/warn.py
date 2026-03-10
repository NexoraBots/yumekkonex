from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Yumeko.database import warn_db
from Yumeko import app
from Yumeko.helper.user import resolve_user , RESTRICT
from Yumeko.decorator.chatadmin import can_restrict_members
from pyrogram.enums import ParseMode
from pyrogram.errors import ChatAdminRequired
from config import config
from pyrogram.enums import ChatMemberStatus
from Yumeko.decorator.save import save 
from Yumeko.decorator.errors import error


MAX_WARNS = warn_db.MAX_WARNS


@app.on_message(filters.command("warn" , prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def warn_user(client: Client, message: Message):

    try:

        if len(message.command) < 2 and not message.reply_to_message:
            await message.reply(
                "<b>𝖴𝗌𝖺𝗀𝖾:</b> 𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗈𝗋 𝗆𝖾𝗇𝗍𝗂𝗈𝗇 𝗍𝗁𝖾𝗆 𝗍𝗈 𝗂𝗌𝗌𝗎𝖾 𝖺 𝗐𝖺𝗋𝗇𝗂𝗇𝗀.\n"
                "<b>𝖤𝗑𝖺𝗆𝗉𝗅𝖾:</b> <code>/𝗐𝖺𝗋𝗇 @𝗎𝗌𝖾𝗋 𝖲𝗉𝖺𝗆𝗆𝗂𝗇𝗀</code>",
                parse_mode=ParseMode.HTML
            )
            return
    
        reason = " ".join(message.command[2:]) if len(message.command) > 2 else "𝖭𝗈 𝗋𝖾𝖺𝗌𝗈𝗇 𝗉𝗋𝗈𝗏𝗂𝖽𝖾𝖽."
        target_user = await resolve_user(client, message)
    
        if not target_user:
            await message.reply("<b>𝖤𝗋𝗋𝗈𝗋:</b> 𝖴𝗇𝖺𝖻𝗅𝖾 𝗍𝗈 𝗂𝖽𝖾𝗇𝗍𝗂𝖿𝗒 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋.", parse_mode=ParseMode.HTML)
            return

        x = await app.get_chat_member(message.chat.id, target_user.id)
    
        if x.status == ChatMemberStatus.OWNER:
            await message.reply("𝖧𝗈𝗐 𝖢𝖺𝗇 𝖨 Warn 𝖳𝗁𝖾 𝖮𝗐𝗇𝖾𝗋?")
            return
    
        if x.status == ChatMemberStatus.ADMINISTRATOR:
            await message.reply("𝖴𝗌𝖾𝗋 𝖨𝗌 𝖠𝖽𝗆𝗂𝗇!")
            return
    
        warn_count = await warn_db.add_warn(message.chat.id, target_user.id, reason, client)
        user_mention = target_user.mention
    
        if warn_count >= MAX_WARNS:
            await message.reply(
                f"**𝖴𝗌𝖾𝗋 𝖡𝖺𝗇𝗇𝖾𝖽:** {user_mention}\n"
                f"**𝖱𝖾𝖺𝗌𝗈𝗇:** {reason}\n"
                f"**𝖶𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝖤𝗑𝖼𝖾𝖾𝖽𝖾𝖽:** {MAX_WARNS}"
            )
            return
    
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("- 1", callback_data=f"warn_decrease_{target_user.id}"),
                InlineKeyboardButton("+ 1", callback_data=f"warn_increase_{target_user.id}")
            ],
            [InlineKeyboardButton("𝖢𝗅𝖾𝖺𝗋 𝖠𝗅𝗅 𝖶𝖺𝗋𝗇𝗂𝗇𝗀𝗌", callback_data=f"warn_delete_{target_user.id}")],
            [InlineKeyboardButton("🗑️", callback_data="delete")]
        ])
    
        await message.reply(
            f"**𝖶𝖺𝗋𝗇𝗂𝗇𝗀 𝖨𝗌𝗌𝗎𝖾𝖽:** {user_mention}\n"
            f"**𝖱𝖾𝖺𝗌𝗈𝗇:** {reason}\n"
            f"**𝖢𝗎𝗋𝗋𝖾𝗇𝗍 𝖶𝖺𝗋𝗇𝗂𝗇𝗀𝗌:** {warn_count} / {MAX_WARNS}",
            reply_markup=keyboard
        )

        await app.restrict_chat_member(message.chat.id , target_user.id , permissions=RESTRICT)

    except ChatAdminRequired:
        await message.reply_text("Chat ADMIN REQUIRED")


@app.on_message(filters.command("setwarnlimit", prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def set_warn_limit(client: Client, message: Message):

    if len(message.command) < 2:
        return await message.reply(
            "<b>𝖴𝗌𝖺𝗀𝖾:</b> /𝗌𝖾𝗍𝗐𝖺𝗋𝗇𝗅𝗂𝗆𝗂𝗍 <number>",
            parse_mode=ParseMode.HTML
        )

    try:
        limit = int(message.command[1])

        await warn_db.set_warn_limit(message.chat.id, limit)

        await message.reply(
            f"<b>𝖶𝖺𝗋𝗇 𝖫𝗂𝗆𝗂𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝖽</b>\n"
            f"<b>𝖭𝖾𝗐 𝖫𝗂𝗆𝗂𝗍:</b> {limit}",
            parse_mode=ParseMode.HTML
        )

    except ValueError:
        await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗇𝗎𝗆𝖻𝖾𝗋.")


@app.on_message(filters.command("resetwarns", prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def reset_warns(client: Client, message: Message):

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply(
            "<b>𝖴𝗌𝖺𝗀𝖾:</b> 𝖱𝖾𝗉𝗅𝗒 𝗈𝗋 /𝗋𝖾𝗌𝖾𝗍𝗐𝖺𝗋𝗇𝗌 <user>",
            parse_mode=ParseMode.HTML
        )

    target_user = await resolve_user(client, message)

    if not target_user:
        return await message.reply("<b>𝖴𝗌𝖾𝗋 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽.</b>", parse_mode=ParseMode.HTML)

    await warn_db.clear_warns(message.chat.id, target_user.id)

    await message.reply(
        f"<b>𝖠𝗅𝗅 𝖶𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝖱𝖾𝗌𝖾𝗍</b>\n"
        f"<b>𝖴𝗌𝖾𝗋:</b> {target_user.mention}",
        parse_mode=ParseMode.HTML
    )


@app.on_message(filters.command("unwarn" , prefixes=config.COMMAND_PREFIXES) & filters.group)
@can_restrict_members
@error
@save
async def unwarn_user(client: Client, message: Message):

    try:

        target_user = await resolve_user(client, message)

        if not target_user:
            return await message.reply("<b>𝖴𝗌𝖾𝗋 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽.</b>", parse_mode=ParseMode.HTML)

        warn_count = await warn_db.remove_warn(message.chat.id, target_user.id)

        if warn_count == 0:
            await message.reply(
                f"**𝖭𝗈 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗍𝗈 𝗋𝖾𝗆𝗈𝗏𝖾 𝖿𝗈𝗋:** {target_user.mention}"
            )
            return
    
        await message.reply(
            f"**𝖶𝖺𝗋𝗇𝗂𝗇𝗀 𝗋𝖾𝗆𝗈𝗏𝖾𝖽:** {target_user.mention}\n"
            f"**𝖱𝖾𝗆𝖺𝗂𝗇𝗂𝗇𝗀:** {warn_count}"
        )

    except ChatAdminRequired:
        await message.reply_text("Chat ADMIN REQUIRED")


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
