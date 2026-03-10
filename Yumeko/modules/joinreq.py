from pyrogram import filters , Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import CallbackQuery, ChatJoinRequest
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

    kb = [
        [
            ikb("Accept", f"accept_joinreq_{user}"),
            ikb("Decline", f"decline_joinreq_{user}")
        ]
    ]

    await c.send_message(chat, txt, reply_markup=ikm(kb))


@app.on_callback_query(filters.regex("^accept_joinreq_uest_") | filters.regex("^decline_joinreq_uest_"))
async def accept_decline_request(c: Client, q: CallbackQuery):
    user_id = q.from_user.id
    chat = q.message.chat.id
    try:
        user_status = (await q.message.chat.get_member(user_id)).status
        if user_status not in {CMS.OWNER, CMS.ADMINISTRATOR}:
            await q.answer(
                "You're not even an admin, don't try this explosive shit!",
                show_alert=True,
            )
            return
    except Exception:
        await q.answer("Unknow error occured. You are not admin or owner")
        return
    split = q.data.split("_")
    chat = q.message.chat.id
    user = int(split[-1])
    data = split[0]
    try:
        userr = await c.get_users(user)
    except Exception:
        userr = None
    if data == "accept":
        try:
            await c.approve_chat_join_request(chat, user)
            await q.answer(f"Accepted join request of the {userr.mention if userr else user}", True)
            await q.edit_message_text(f"{q.from_user.mention} accepted join request of {userr.mention if userr else user}")
        except Exception :
            return
    elif data == "decline":
        try:
            await c.decline_chat_join_request(chat, user)
            await q.answer(f"DECLINED: {user}")
            await q.edit_message_text(f"{q.from_user.mention} declined join request of {userr.mention if userr else user}")
        except Exception :
            return
    return


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
