from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from pyrogram import filters
from pyrogram.types import Message
from Yumeko import app
from config import config
from Yumeko.decorator.errors import error
from Yumeko.decorator.save import save


@app.on_message(filters.command("check_mongo", prefixes=config.COMMAND_PREFIXES) & filters.user(config.OWNER_ID))
@error
@save
async def check_mongo(client, message: Message):
    
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.reply_text(
            "❌ **Usage:** `/check_mongo mongodb_uri`\n\n"
            "Example:\n"
            "`/check_mongo mongodb+srv://user:pass@cluster.mongodb.net/db`"
        )
        return

    uri = args[1]

    msg = await message.reply_text("🔍 **Checking MongoDB connection...**")

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        # ping the database
        client.admin.command("ping")

        await msg.edit_text(
            "✅ **MongoDB Connection Successful!**\n\n"
            "• URI is valid\n"
            "• Database reachable\n"
            "• Authentication passed"
        )

    except ConfigurationError:
        await msg.edit_text(
            "❌ **Invalid MongoDB URI format.**"
        )

    except ConnectionFailure:
        await msg.edit_text(
            "❌ **Connection failed.**\n"
            "• Server not reachable\n"
            "• Wrong credentials\n"
            "• Network issue"
        )

    except Exception as e:
        await msg.edit_text(
            f"⚠️ **Unexpected Error:**\n`{str(e)}`"
        )
