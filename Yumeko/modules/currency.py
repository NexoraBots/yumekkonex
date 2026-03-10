from pyrogram import Client, filters
from pyrogram.types import Message
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error
import aiohttp

__module__ = "𝖢𝗎𝗋𝗋𝖾𝗇𝖼𝗒"

__help__ = """
𝖢𝗈𝗇𝗏𝖾𝗋𝗍 𝖻𝖾𝗍𝗐𝖾𝖾𝗇 𝖽𝗂𝖿𝖿𝖾𝗋𝖾𝗇𝗍 𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗂𝖾𝗌.

𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:
• /𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒 [𝖺𝗆𝗈𝗎𝗇𝗍] [𝖿𝗋𝗈𝗆] [𝗍𝗈]
• /𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒 𝗅𝗂𝗌𝗍

𝖤𝗑𝖺𝗆𝗉𝗅𝖾𝗌:
• /𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒 100 USD EUR
• /𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒 50 JPY INR
"""


API = "https://open.er-api.com/v6/latest/"


async def get_rates(base):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API}{base}") as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("rates", {})
            return {}


@app.on_message(filters.command("𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒", prefixes=config.COMMAND_PREFIXES))
@save
@error
async def currency_converter(client: Client, message: Message):

    args = message.text.split()

    if len(args) == 2 and args[1].lower() == "list":

        rates = await get_rates("USD")

        if not rates:
            return await message.reply_text("❌ 𝖢𝗈𝗎𝗅𝖽𝗇'𝗍 𝖿𝖾𝗍𝖼𝗁 𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒 𝗅𝗂𝗌𝗍.")

        currency_list = ", ".join(sorted(rates.keys())[:50])

        return await message.reply_text(
            f"💱 **𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖢𝗎𝗋𝗋𝖾𝗇𝖼𝗂𝖾𝗌**\n\n"
            f"{currency_list}\n\n"
            f"Use `/𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒 100 USD INR`"
        )

    if len(args) != 4:
        return await message.reply_text(
            "💱 **𝖢𝗎𝗋𝗋𝖾𝗇𝖼𝗒 𝖢𝗈𝗇𝗏𝖾𝗋𝗍𝖾𝗋**\n\n"
            "Usage:\n"
            "`/𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒 100 USD INR`"
        )

    try:
        amount = float(args[1])
        base = args[2].upper()
        target = args[3].upper()

    except ValueError:
        return await message.reply_text("❌ 𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖺𝗆𝗈𝗎𝗇𝗍.")

    rates = await get_rates(base)

    if not rates:
        return await message.reply_text("❌ 𝖢𝗈𝗎𝗅𝖽𝗇'𝗍 𝖿𝖾𝗍𝖼𝗁 𝖾𝗑𝖼𝗁𝖺𝗇𝗀𝖾 𝗋𝖺𝗍𝖾.")

    if target not in rates:
        return await message.reply_text("❌ 𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗍𝖺𝗋𝗀𝖾𝗍 𝖼𝗎𝗋𝗋𝖾𝗇𝖼𝗒.")

    result = amount * rates[target]

    await message.reply_text(
        f"💱 **𝖢𝗎𝗋𝗋𝖾𝗇𝖼𝗒 𝖢𝗈𝗇𝗏𝖾𝗋𝗌𝗂𝗈𝗇**\n\n"
        f"**{amount} {base}** = **{round(result,2)} {target}**"
    )
