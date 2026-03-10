import aiohttp
from pyrogram import filters
from Yumeko import app
from config import config
from pyrogram.enums import ParseMode
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error

NEWS_API_KEY = "pub_00ec9c08bcfe4755a8bef099c51a5087"


@app.on_message(filters.command("news", prefixes=config.COMMAND_PREFIXES))
@error
@save
async def news_command(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗄𝖾𝗒𝗐𝗈𝗋𝖽.\n"
            "𝖤𝗑𝖺𝗆𝗉𝗅𝖾: `/news anime`",
            parse_mode=ParseMode.MARKDOWN
        )

    keyword = " ".join(message.command[1:])

    api_url = (
        f"https://newsdata.io/api/1/news?"
        f"apikey={NEWS_API_KEY}&q={keyword}&language=en"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:

                if response.status != 200:
                    return await message.reply_text(
                        "𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝖿𝖾𝗍𝖼𝗁 𝗇𝖾𝗐𝗌."
                    )

                data = await response.json()

        results = data.get("results", [])

        if not results:
            return await message.reply_text(
                f"𝖭𝗈 𝗇𝖾𝗐𝗌 𝖿𝗈𝗎𝗇𝖽 𝖿𝗈𝗋 **{keyword}**.",
                parse_mode=ParseMode.MARKDOWN
            )

        text = f"**𝖭𝖾𝗐𝗌 𝗋𝖾𝗌𝗎𝗅𝗍𝗌 𝖿𝗈𝗋: {keyword}**\n\n"

        for article in results[:5]:
            title = article.get("title", "No title")
            link = article.get("link", "")
            source = article.get("source_id", "Unknown")

            text += f"• [{title}]({link})\n  𝖲𝗈𝗎𝗋𝖼𝖾: {source}\n\n"

        await message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

    except Exception as e:
        print(f"News Error: {e}")
        await message.reply_text(
            "𝖠𝗇 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽 𝗐𝗁𝗂𝗅𝖾 𝖿𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝗇𝖾𝗐𝗌."
        )


__module__ = "𝖭𝖾𝗐𝗌"


__help__ = """
𝖳𝗁𝗂𝗌 𝗆𝗈𝖽𝗎𝗅𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾𝗌 𝗌𝖾𝖺𝗋𝖼𝗁 𝖿𝗎𝗇𝖼𝗍𝗂𝗈𝗇𝖺𝗅𝗂𝗍𝗂𝖾𝗌 𝖿𝗈𝗋 𝗇𝖾𝗐𝗌, 𝖡𝗂𝗇𝗀 𝗌𝖾𝖺𝗋𝖼𝗁, 𝖺𝗇𝖽 𝗂𝗆𝖺𝗀𝖾 𝗌𝖾𝖺𝗋𝖼𝗁𝖾𝗌.
  
𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:
𝟣. /𝗇𝖾𝗐𝗌 <𝗄𝖾𝗒𝗐𝗈𝗋𝖽> - 𝖲𝖾𝖺𝗋𝖼𝗁 𝖿𝗈𝗋 𝗇𝖾𝗐𝗌 𝖺𝗋𝗍𝗂𝖼𝗅𝖾𝗌 𝖻𝖺𝗌𝖾𝖽 𝗈𝗇 𝖺 𝗄𝖾𝗒𝗐𝗈𝗋𝖽. 
     𝖤𝗑𝖺𝗆𝗉𝗅𝖾: /𝗇𝖾𝗐𝗌 𝖿𝗈𝗈𝗍𝖻𝖺𝗅𝗅

𝖭𝗈𝗍𝖾: 
- 𝖥𝗈𝗋 /𝗇𝖾𝗐𝗌, 𝗒𝗈𝗎 𝖼𝖺𝗇 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺𝗇𝗒 𝗄𝖾𝗒𝗐𝗈𝗋𝖽 𝗈𝗋 𝗅𝖾𝖺𝗏𝖾 𝗂𝗍 𝖾𝗆𝗉𝗍𝗒 𝗍𝗈 𝖿𝖾𝗍𝖼𝗁 𝗀𝖾𝗇𝖾𝗋𝖺𝗅 𝗇𝖾𝗐𝗌.
"""

