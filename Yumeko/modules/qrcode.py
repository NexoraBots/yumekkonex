import qrcode
from io import BytesIO
from pyrogram import filters
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error


@app.on_message(filters.command("qrcode", prefixes=config.COMMAND_PREFIXES))
@error
@save
async def generate_qr(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗍𝖾𝗑𝗍 𝗈𝗋 𝖴𝖱𝖫.\n"
            "𝖤𝗑𝖺𝗆𝗉𝗅𝖾: `/qrcode https://google.com`"
        )

    data = message.text.split(None, 1)[1]

    try:

        qr = qrcode.make(data)

        bio = BytesIO()
        bio.name = "qrcode.png"
        qr.save(bio, "PNG")
        bio.seek(0)

        await message.reply_photo(
            bio,
            caption="𝖧𝖾𝗋𝖾 𝗂𝗌 𝗒𝗈𝗎𝗋 𝖰𝖱 𝖼𝗈𝖽𝖾."
        )

    except Exception:
        await message.reply_text(
            "𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝖰𝖱 𝖼𝗈𝖽𝖾."
        )


__module__ = "𝖰𝖱 𝖢𝗈𝖽𝖾"


__help__ = """
𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝖰𝖱 𝖼𝗈𝖽𝖾𝗌 𝖿𝗋𝗈𝗆 𝗍𝖾𝗑𝗍 𝗈𝗋 𝖴𝖱𝖫𝗌.

**𝖢𝗈𝗆𝗆𝖺𝗇𝖽:**
• /qrcode <text/url>

**𝖤𝗑𝖺𝗆𝗉𝗅𝖾:**
• /qrcode https://google.com
• /qrcode Hello World
"""
