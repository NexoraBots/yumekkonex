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

        await client.leave_chat(chat_id)

        await message.reply_text(
            f"𝖫𝖾𝖿𝗍 **{chat.title}**."
        )

        await client.send_message(
            config.OWNER_ID,
            f"𝖡𝗈𝗍 𝗁𝖺𝗌 𝗅𝖾𝖿𝗍 𝖼𝗁𝖺𝗍:\n\n"
            f"**{chat.title}**\n"
            f"`{chat.id}`"
        )

    except Exception as e:
        await message.reply_text(
            "𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗅𝖾𝖺𝗏𝖾 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍."
        )
        print(e)
