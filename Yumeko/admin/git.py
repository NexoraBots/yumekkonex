import os
import subprocess
import sys
from pyrogram import filters
from Yumeko import app
from config import config
from Yumeko.helper.on_start import save_restart_data
from Yumeko.decorator.errors import error
from Yumeko.decorator.save import save

REPO_URL = "https://github.com/NexoraBots/yumekkonex"
BRANCH = "main"


@app.on_message(filters.command("update", prefixes=config.COMMAND_PREFIXES) & filters.user(config.OWNER_ID))
@app.on_message(filters.regex(r"(?i)^Yumeko Update$") & filters.user(config.OWNER_ID))
@error
@save
async def git_pull_command(client, message):
    try:
        await message.reply("🔄 **Checking for updates...**")

        # Ensure git repo exists
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)

        # Fetch updates
        subprocess.run(["git", "fetch", "origin"], check=True)

        result = subprocess.run(
            ["git", "pull", "origin", BRANCH],
            capture_output=True,
            text=True
        )

        if "Already up to date" in result.stdout:
            await message.reply("✅ **Repository is already up to date.**")
            return

        # Install new requirements if changed
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        restart_message = await message.reply(
            "✅ **Update successful!**\n\n🔁 **Restarting Yumeko...**"
        )

        save_restart_data(restart_message.chat.id, restart_message.id)
        await restart_bot()

    except Exception as e:
        await message.reply(f"❌ **Update failed:**\n`{str(e)}`")


async def restart_bot():
    os.execvp(sys.executable, [sys.executable, "-m", "Yumeko"])


@app.on_message(filters.command("restart", prefixes=config.COMMAND_PREFIXES) & filters.user(config.OWNER_ID))
@error
@save
async def restart_command(client, message):
    try:
        restart_message = await message.reply("🔁 **Restarting Yumeko...**")
        save_restart_data(restart_message.chat.id, restart_message.id)
        os.execvp(sys.executable, [sys.executable, "-m", "Yumeko"])
    except Exception as e:
        await message.reply(f"❌ Restart failed: `{str(e)}`")
