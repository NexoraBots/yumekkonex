import time
import psutil
import platform
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import config
from Yumeko import app, start_time, start_time_str
import pyrogram
import telethon
import motor
from telegram import __version__ as ptb_version

@app.on_message(filters.command("alive", config.COMMAND_PREFIXES))
async def alive_command(client: Client, message: Message):
    # --- Calculate uptime ---
    uptime_seconds = int(time.time() - start_time)
    uptime_str = time.strftime("%Hh %Mm %Ss", time.gmtime(uptime_seconds))

    # --- System stats ---
    cpu_usage = psutil.cpu_percent(interval=0.5)
    memory_usage = psutil.virtual_memory().percent

    # --- Ping ---
    start_ping = time.time()
    ping_message = await message.reply_text("🏓 Pinging...")
    end_ping = time.time()
    ping = round((end_ping - start_ping) * 1000, 2)

    # --- Styled message ---
    alive_text = (
        f"🌟 **『 {app.me.first_name} is Online! 』** 🌟\n\n"
        f"**💡 Uptime:** `{uptime_str}`\n"
        f"**🛠 Bot Version:** `{config.BOT_VERSION}`\n\n"
        f"⚙️ **System Stats:**\n"
        f"• CPU: `{cpu_usage}%`\n"
        f"• Memory: `{memory_usage}%`\n"
        f"• Ping: `{ping} ms`\n"
        f"• Started at: `{start_time_str}`\n\n"
        f"📌 **Notes:**\n"
        f"I am online and ready to manage your groups. Use `/help` to explore commands!"
    )

    # --- Buttons ---
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🤝 Support", url=config.SUPPORT_CHAT_LINK),
            InlineKeyboardButton("⚡ Version Info", callback_data="version_info")
        ],
        [
            InlineKeyboardButton("👤 Owner", user_id=config.OWNER_ID)
        ]
    ])

    # --- Edit ping message ---
    await ping_message.edit_text(alive_text, reply_markup=buttons, disable_web_page_preview=True)


@app.on_callback_query(filters.regex("version_info"))
async def version_info_callback(client: Client, callback_query):
    # --- Library versions ---
    pyro_ver = pyrogram.__version__
    telethon_ver = telethon.__version__
    motor_ver = motor.version
    python_ver = platform.python_version()

    # --- Formatted version info ---
    version_text = (
        f"⚡ **Bot Version:** `{config.BOT_VERSION}`\n"
        f"📦 **Pyrogram:** `{pyro_ver}`\n"
        f"📦 **Telethon:** `{telethon_ver}`\n"
        f"📦 **PTB:** `{ptb_version}`\n"
        f"📦 **Motor:** `{motor_ver}`\n"
        f"🐍 **Python:** `{python_ver}`"
    )

    # Show as alert (popup)
    await callback_query.answer(version_text, show_alert=True)
