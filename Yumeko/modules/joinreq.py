from pyrogram import filters , Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import CallbackQuery, ChatJoinRequest, Message
from pyrogram.types import InlineKeyboardButton as ikb
from pyrogram.types import InlineKeyboardMarkup as ikm
from Yumeko import app , JOIN_UPDATE_GROUP
from Yumeko.database.joinreq_db import (
    enable_joinreq,
    disable_joinreq,
    is_joinreq_enabled
)
from config import config


@app.on_message(filters.command("request", prefixes=config.COMMAND_PREFIXES) & filters.group)
async def request_toggle(client: Client, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "𝖴𝗌𝖺𝗀𝖾:\n"
            "/request enable\n"
            "/request disable"
        )

    chat_id = message.chat.id
    option = message.command[1].lower()

    member = await message.chat.get_member(message.from_user.id)

    if member.status not in [CMS.ADMINISTRATOR, CMS.OWNER]:
        return await message.reply_text(
            "𝖮𝗇𝗅𝗒 𝖺𝖽𝗆𝗂𝗇𝗌 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽."
        )

    if option == "enable":
        await enable_joinreq(chat_id)
        await message.reply_text(
            "𝖩𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗆𝖺𝗇𝖺𝗀𝖾𝗋 𝖾𝗇𝖺𝖻𝗅𝖾𝖽."
        )

    elif option == "disable":
        await disable_joinreq(chat_id)
        await message.reply_text(
            "𝖩𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗆𝖺𝗇𝖺𝗀𝖾𝗋 𝖽𝗂𝗌𝖺𝖻𝗅𝖾𝖽."
        )

    else:
        await message.reply_text(
            "𝖴𝗌𝖾: enable / disable"
        )

@app.on_chat_join_request(group=JOIN_UPDATE_GROUP)
async def join_request_handler(c: Client, j: ChatJoinRequest):

    chat = j.chat.id

    if not await is_joinreq_enabled(chat):
        return

    user = j.from_user.id
    userr = j.from_user

    txt = (
        "𝖭𝖾𝗐 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍\n\n"
        "**𝖴𝗌𝖾𝗋 𝖨𝗇𝖿𝗈**\n"
        f"𝖭𝖺𝗆𝖾: {userr.full_name}\n"
        f"𝖬𝖾𝗇𝗍𝗂𝗈𝗇: {userr.mention}\n"
        f"𝖨𝖣: `{user}`\n"
        f"𝖲𝖼𝖺𝗆: {'True' if userr.is_scam else 'False'}\n"
    )

    if userr.username:
        txt += f"𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: @{userr.username}\n"

    kb = [[
        ikb("Accept", f"accept_joinreq_{user}"),
        ikb("Decline", f"decline_joinreq_{user}")
    ]]

    await c.send_message(chat, txt, reply_markup=ikm(kb))


@app.on_callback_query(filters.regex("^(accept|decline)_joinreq_"))
async def accept_decline_request(c: Client, q: CallbackQuery):

    admin = q.from_user.id
    chat = q.message.chat.id

    try:
        status = (await q.message.chat.get_member(admin)).status
        if status not in {CMS.OWNER, CMS.ADMINISTRATOR}:
            return await q.answer(
                "𝖮𝗇𝗅𝗒 𝖺𝖽𝗆𝗂𝗇𝗌 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌.",
                show_alert=True
            )
    except:
        return await q.answer("𝖤𝗋𝗋𝗈𝗋 𝖼𝗁𝖾𝖼𝗄𝗂𝗇𝗀 𝖺𝖽𝗆𝗂𝗇.", True)

    data = q.data.split("_")
    action = data[0]
    user = int(data[-1])

    try:
        userr = await c.get_users(user)
        mention = userr.mention
    except:
        mention = f"`{user}`"

    try:

        if action == "accept":
            await c.approve_chat_join_request(chat, user)
            text = f"{q.from_user.mention} 𝖺𝖼𝖼𝖾𝗉𝗍𝖾𝖽 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗈𝖿 {mention}"

        else:
            await c.decline_chat_join_request(chat, user)
            text = f"{q.from_user.mention} 𝖽𝖾𝖼𝗅𝗂𝗇𝖾𝖽 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗈𝖿 {mention}"

    except Exception as e:

        if "USER_ALREADY_PARTICIPANT" in str(e):
            text = f"{mention} 𝗂𝗌 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗂𝗇 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉."

        elif "INVITE_REQUEST_SENT" in str(e):
            text = f"{mention} 𝗁𝖺𝗌 𝗇𝗈 𝗉𝖾𝗇𝖽𝗂𝗇𝗀 𝗋𝖾𝗊𝗎𝖾𝗌𝗍."

        else:
            text = f"𝖤𝗋𝗋𝗈𝗋: {e}"

    try:
        await q.message.edit_text(text)
    except:
        try:
            await q.message.delete()
            await c.send_message(chat, text)
        except:
            pass

    await q.answer()

__module__ = "𝖩𝗈𝗂𝗇 𝖱𝖾𝗊𝗎𝖾𝗌𝗍"


__help__ = """**𝖩𝗈𝗂𝗇 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖬𝖺𝗇𝖺𝗀𝖾𝗆𝖾𝗇𝗍**

𝖬𝖺𝗇𝖺𝗀𝖾 𝗎𝗌𝖾𝗋 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝗌 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉𝗌 𝗐𝗂𝗍𝗁 𝖺𝗉𝗉𝗋𝗈𝗏𝖺𝗅 𝖾𝗇𝖺𝖻𝗅𝖾𝖽.

**𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**
✧ /request enable — 𝖤𝗇𝖺𝖻𝗅𝖾 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗆𝖺𝗇𝖺𝗀𝖾𝗋  
✧ /request disable — 𝖣𝗂𝗌𝖺𝖻𝗅𝖾 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗆𝖺𝗇𝖺𝗀𝖾𝗋  

**𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌:**
✧ 𝖭𝗈𝗍𝗂𝖿𝗂𝖾𝗌 𝗐𝗁𝖾𝗇 𝖺 𝗇𝖾𝗐 𝗃𝗈𝗂𝗇 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝖺𝗋𝗋𝗂𝗏𝖾𝗌  
✧ 𝖲𝗁𝗈𝗐𝗌 𝗎𝗌𝖾𝗋 𝗂𝗇𝖿𝗈 (𝖭𝖺𝗆𝖾, 𝖨𝖣, 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾, 𝖲𝖼𝖺𝗆 𝗌𝗍𝖺𝗍𝗎𝗌)  
✧ 𝖠𝖽𝗆𝗂𝗇𝗌 𝖼𝖺𝗇 𝖺𝖼𝖼𝖾𝗉𝗍 𝗈𝗋 𝖽𝖾𝖼𝗅𝗂𝗇𝖾 𝗏𝗂𝖺 𝖻𝗎𝗍𝗍𝗈𝗇𝗌
"""
