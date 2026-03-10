from Yumeko import app , CHATBOT_GROUP
from Yumeko.database.chatbotdb import enable_chatbot , disable_chatbot , is_chatbot_enabled
from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery , InlineKeyboardButton , InlineKeyboardMarkup
from config import config 
from Yumeko.decorator.chatadmin import chatadmin
from pyrogram.enums import ChatAction
import httpx  
from Yumeko.decorator.save import save 
from Yumeko.decorator.errors import error

# Command to toggle announcement status
@app.on_message(filters.command("chatbot" , prefixes=config.COMMAND_PREFIXES) & filters.group)
@chatadmin
@error
@save
async def chatbot_handler(client: Client, message: Message):
    chat_id = message.chat.id
        
    if await is_chatbot_enabled(chat_id):
        # If already enabled, send a button to disable
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔴 𝖣𝗂𝗌𝖺𝖻𝗅𝖾 𝖢𝗁𝖺𝗍𝖡𝗈𝗍", callback_data=f"disable_chatbot:{chat_id}")],
            [InlineKeyboardButton("🗑️", callback_data="delete")]]
        )
        await message.reply_text("**📢 𝖢𝗁𝖺𝗍𝖡𝗈𝗍 𝗂𝗌 𝖾𝗇𝖺𝖻𝗅𝖾𝖽 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍.**", reply_markup=button)
    else:
        # If not enabled, send a button to enable
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🟢 𝖤𝗇𝖺𝖻𝗅𝖾 𝖢𝗁𝖺𝗍𝖡𝗈𝗍", callback_data=f"enable_chatbot:{chat_id}")],
            [InlineKeyboardButton("🗑️", callback_data="delete")]]
             
        )
        await message.reply_text("**📢 𝖢𝗁𝖺𝗍𝖡𝗈𝗍 𝗂𝗌 𝖽𝗂𝗌𝖺𝖻𝗅𝖾𝖽 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍.**", reply_markup=button)


# Callback query handler to enable/disable announcements
@app.on_callback_query(filters.regex("^(enable_chatbot|disable_chatbot):"))
@chatadmin
@error
async def toggle_announcements(client: Client, callback_query : CallbackQuery):
    action, chat_id = callback_query.data.split(":")
    chat_id = int(chat_id)
    chat = await client.get_chat(chat_id)

    if action == "enable_chatbot":
        await enable_chatbot(chat_id, chat.title, chat.username)
        await callback_query.message.edit_text("**🟢 𝖢𝗁𝖺𝗍𝖡𝗈𝗍 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖾𝗇𝖺𝖻𝗅𝖾𝖽 𝖿𝗈𝗋 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍.**")
    elif action == "disable_chatbot":
        await disable_chatbot(chat_id)
        await callback_query.message.edit_text("**🔴 𝖢𝗁𝖺𝗍𝖡𝗈𝗍 𝗁𝖺𝗏𝖾 𝖻𝖾𝖾𝗇 𝖽𝗂𝗌𝖺𝖻𝗅𝖾𝖽 𝖿𝗈𝗋 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍.**")

@app.on_message(filters.group | (filters.private & filters.reply), group=CHATBOT_GROUP)
@error
@save
async def handle_chatbot(client: Client, message: Message):

    if not message.from_user:
        return

    if not await is_chatbot_enabled(message.chat.id):
        return    

    # Ensure it's a reply to the bot
    if message.reply_to_message and message.reply_to_message.from_user:
        if message.reply_to_message.from_user.id != config.BOT_ID:
            return  # Not replying to the bot, ignore
    else:
        return  # No reply or missing from_user, ignore

    await client.send_chat_action(message.chat.id, action=ChatAction.TYPING)

    m = message.text

    bot_response = None  # Initialize

    # Fetch chatbot response from API asynchronously
    try:
        async with httpx.AsyncClient(timeout=15) as client_http:
            kuki_response = await client_http.get(
                "http://api.brainshop.ai/get",
                params={
                    "bid": 176809,
                    "key": "lbMN8CXTGzhn1NKG",
                    "uid": message.from_user.id,
                    "msg": m,
                }
            )
            # Raise for non-200 responses
            kuki_response.raise_for_status()

            # Parse JSON safely
            try:
                response_data = kuki_response.json()
                bot_response = response_data.get("cnt")
            except Exception as e_json:
                print(f"𝖤𝗋𝗋𝗈𝗋 𝗉𝖺𝗋𝗌𝗂𝗇𝗀 𝖠𝗉𝗂 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾: {e_json}")
                bot_response = None

            # Treat empty strings as failure
            if not bot_response:
                bot_response = None

    except httpx.RequestError as e:
        print(f"𝖤𝗋𝗋𝗈𝗋 𝖿𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝖼𝗁𝖺𝗍𝖻𝗈𝗍 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾: {e}")
        bot_response = None
    except httpx.HTTPStatusError as e:
        print(f"𝖠𝗣𝗜 𝗋𝖾𝗍𝗎𝗋𝗇𝖾𝖽 𝗇𝗈𝗇-200 𝗌𝗍𝖺𝗍𝗎𝗌: {e}")
        bot_response = None
    except Exception as e:
        print(f"Unexpected error: {e}")
        bot_response = None

    # Disable chatbot if response failed
    if bot_response is None:
        await message.reply_text(
            "❌ 𝖢𝗁𝖺𝗍𝖻𝗈𝗍 𝗂𝗌 𝖿𝖺𝖼𝗂𝗇𝗀 𝗂𝗌𝗌𝗎𝖾𝗌 𝖺𝗇𝖽 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖽𝗂𝗌𝖺𝖻𝗅𝖾𝖽 𝖿𝗈𝗋 𝗇𝗈𝗐. 𝖯𝗅𝖾𝖺𝗌𝖾 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗌𝗎𝗉𝗉𝗈𝗋𝗍."
        )
        await disable_chatbot(message.chat.id)
        return

    # Reply to the user's message
    await message.reply_text(bot_response)
    
__module__ = "𝖢𝗁𝖺𝗍𝖻𝗈𝗍"

__help__ = "✧ /𝖼𝗁𝖺𝗍𝖻𝗈𝗍 : 𝖴𝗌𝖾 𝖨𝗍 𝖳𝗈 𝖤𝗇𝖺𝖻𝗅𝖾 𝖮𝗋 𝖣𝗂𝗌𝖺𝖻𝗅𝖾 𝖢𝗁𝖺𝗍𝖻𝗈𝗍 𝖨𝗇 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉."
