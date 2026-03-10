from pyrogram import Client, filters
from pyrogram.types import Message
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error
from sympy import sympify
from sympy import sin, cos, tan, sqrt, log
import math


def calculate_expression(expression: str):

    try:
        result = sympify(expression).evalf()
        return result
    except Exception:
        return None

@app.on_message(filters.command(["calculate", "calc"], prefixes=config.COMMAND_PREFIXES))
@save
@error
async def calculator(client: Client, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "📐 **𝖢𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗈𝗋**\n"
            "𝖯𝖾𝗋𝖿𝗈𝗋𝗆 𝗆𝖺𝗍𝗁𝖾𝗆𝖺𝗍𝗂𝖼𝖺𝗅 𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗂𝗈𝗇𝗌.\n"
            "**𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:**\n"
            "• `/𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝖾 𝟤+𝟤`\n"
            "• `/𝖼𝖺𝗅𝖼 (𝟧+𝟥)*𝟤`\n"
            "• `/𝖼𝖺𝗅𝖼 𝗌𝗊𝗋𝗍(𝟣𝟨)`\n"
            "• `/𝖼𝖺𝗅𝖼 𝗌𝗂𝗇(𝟥𝟢)`"
        )

    expression = " ".join(message.command[1:])

    result = calculate_expression(expression)

    if result is None:
        return await message.reply_text(
            "❌ **𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖾𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇.**\n"
            "𝖯𝗅𝖾𝖺𝗌𝖾 𝗎𝗌𝖾 𝖺 𝗏𝖺𝗅𝗂𝖽 𝗆𝖺𝗍𝗁 𝖾𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇."
        )

    await message.reply_text(
        f"📊 **𝖢𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗂𝗈𝗇 𝖱𝖾𝗌𝗎𝗅𝗍**\n"
        f"**𝖤𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇:** `{expression}`\n"
        f"**𝖱𝖾𝗌𝗎𝗅𝗍:** `{result}`"
    )

__module__ = "𝖢𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗈𝗋"

__HELP__ = """
𝖯𝖾𝗋𝖿𝗈𝗋𝗆 𝗆𝖺𝗍𝗁𝖾𝗆𝖺𝗍𝗂𝖼𝖺𝗅 𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝗂𝗈𝗇𝗌.

𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:
• /𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝖾 [𝖾𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇] - 𝖢𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝖾 𝗆𝖺𝗍𝗁 𝖾𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇  
• /𝖼𝖺𝗅𝖼 [𝖾𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇] - 𝖲𝗁𝗈𝗋𝗍𝗁𝖺𝗇𝖽 𝖿𝗈𝗋 𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝖾

𝖤𝗑𝖺𝗆𝗉𝗅𝖾𝗌:
• /𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗍𝖾 2 + 2
• /𝖼𝖺𝗅𝖼 (5 + 3) * 2
• /𝖼𝖺𝗅𝖼 sin(30)
• /𝖼𝖺𝗅𝖼 sqrt(16)
"""
