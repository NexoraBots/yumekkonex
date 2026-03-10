from pyrogram import filters
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error


@app.on_message(filters.command("leave", prefixes=config.COMMAND_PREFIXES) & filters.user(config.OWNER_ID))
@error
@save
async def leave_chat(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝖼𝗁𝖺𝗍 𝗂𝖣.\n"
            "𝖤𝗑𝖺𝗆𝗉𝗅𝖾: `/leave -1001234567890`"
        )

    chat_id = message.command[1]

    try:

        chat = await client.get_chat(chat_id)

        leave_text = (
            "✦ **𝖦𝗈𝗈𝖽𝖻𝗒𝖾!**\n\n"
            "𝖳𝗁𝖾 𝖻𝗈𝗍 𝗂𝗌 𝗇𝗈𝗐 𝗅𝖾𝖺𝗏𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍.\n"
            "𝖳𝗁𝖺𝗇𝗄 𝗒𝗈𝗎 𝖿𝗈𝗋 𝗎𝗌𝗂𝗇𝗀 𝗆𝖾.\n\n"
            "✧ 𝖧𝗈𝗉𝖾 𝗐𝖾 𝗆𝖾𝖾𝗍 𝖺𝗀𝖺𝗂𝗇."
        )

        await client.send_message(chat_id, leave_text)

        await client.leave_chat(chat_id)

        await message.reply_text(
            f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗅𝖾𝖿𝗍 **{chat.title}**."
        )

        await client.send_message(
            config.OWNER_ID,
            f"✦ **𝖡𝗈𝗍 𝖫𝖾𝖿𝗍 𝖢𝗁𝖺𝗍**\n\n"
            f"**𝖭𝖺𝗆𝖾:** {chat.title}\n"
            f"**𝖨𝖣:** `{chat.id}`"
        )

    except Exception as e:
        await message.reply_text(
            "𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗅𝖾𝖺𝗏𝖾 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍."
        )
        print(e)
