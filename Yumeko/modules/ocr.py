import pytesseract
from PIL import Image
from pyrogram import filters
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error


@app.on_message(filters.command("ocr", prefixes=config.COMMAND_PREFIXES))
@error
@save
async def ocr_extract(client, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺𝗇 𝗂𝗆𝖺𝗀𝖾 𝗍𝗈 𝖾𝗑𝗍𝗋𝖺𝖼𝗍 𝗍𝖾𝗑𝗍."
        )

    reply = message.reply_to_message

    if not (reply.photo or reply.document):
        return await message.reply_text(
            "𝖯𝗅𝖾𝖺𝗌𝖾 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺𝗇 𝗂𝗆𝖺𝗀𝖾."
        )

    lang = "eng"

    if len(message.command) > 1:
        lang = message.command[1]

    msg = await message.reply_text("𝖤𝗑𝗍𝗋𝖺𝖼𝗍𝗂𝗇𝗀 𝗍𝖾𝗑𝗍...")

    try:

        file_path = await reply.download()

        img = Image.open(file_path)

        text = pytesseract.image_to_string(img, lang=lang)

        if not text.strip():
            return await msg.edit(
                "𝖭𝗈 𝗍𝖾𝗑𝗍 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝗍𝗁𝖾 𝗂𝗆𝖺𝗀𝖾."
            )

        if len(text) > 4000:
            text = text[:4000]

        await msg.edit(
            f"**𝖤𝗑𝗍𝗋𝖺𝖼𝗍𝖾𝖽 𝖳𝖾𝗑𝗍:**\n\n{text}"
        )

    except Exception as e:
        await msg.edit(
            "𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝖾𝗑𝗍𝗋𝖺𝖼𝗍 𝗍𝖾𝗑𝗍."
        )
        print(e)


__module__ = "𝖮𝖢𝖱"


__help__ = """
𝖤𝗑𝗍𝗋𝖺𝖼𝗍 𝗍𝖾𝗑𝗍 𝖿𝗋𝗈𝗆 𝗂𝗆𝖺𝗀𝖾𝗌 𝗎𝗌𝗂𝗇𝗀 𝖮𝖢𝖱.

**𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**
• /ocr — 𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺𝗇 𝗂𝗆𝖺𝗀𝖾 𝗍𝗈 𝖾𝗑𝗍𝗋𝖺𝖼𝗍 𝗍𝖾𝗑𝗍  
• /ocr <lang> — 𝖤𝗑𝗍𝗋𝖺𝖼𝗍 𝗍𝖾𝗑𝗍 𝗂𝗇 𝖺 𝗌𝗉𝖾𝖼𝗂𝖿𝗂𝖼 𝗅𝖺𝗇𝗀𝗎𝖺𝗀𝖾

**𝖤𝗑𝖺𝗆𝗉𝗅𝖾:**
• /ocr  
• /ocr eng
"""
