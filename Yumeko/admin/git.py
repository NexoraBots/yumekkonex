import os
import subprocess
import sys
import asyncio
from datetime import datetime
from pyrogram import filters
from Yumeko import app
from config import config
from Yumeko.helper.on_start import save_restart_data
from Yumeko.decorator.errors import error
from Yumeko.decorator.save import save

REPO_URL = "https://github.com/NexoraBots/yumekkonex"
BRANCH = "master"


@app.on_message(filters.command("update", prefixes=config.COMMAND_PREFIXES) & filters.user(config.OWNER_ID))
@error
@save
async def git_pull_command(client, message):
    try:
        msg = await message.reply("🔄 **Checking for updates...**")

        # Ensure repo exists
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)

        # Fetch latest commits
        subprocess.run(["git", "fetch", "origin"], check=True)

        # Get commit differences
        commits = subprocess.run(
            ["git", "log", f"HEAD..origin/{BRANCH}", "--pretty=format:%h|%an|%s|%ct"],
            capture_output=True,
            text=True
        )

        if not commits.stdout.strip():
            return await msg.edit("✅ **Repository is already up to date.**")

        updates = ""
        repo_link = REPO_URL.replace(".git", "")

        for i, line in enumerate(commits.stdout.splitlines(), start=1):
            sha, author, summary, timestamp = line.split("|")
            date = datetime.fromtimestamp(int(timestamp)).strftime("%d %b %Y")

            updates += (
                f"**➣ #{i}**: [{summary}]({repo_link}/commit/{sha})\n"
                f"   👤 **Author:** {author}\n"
                f"   📅 **Date:** {date}\n\n"
            )

        text = (
            "**✨ New Update Available!**\n\n"
            "**📜 Commits:**\n\n"
            f"{updates}\n"
            "⬇️ **Pulling updates now...**"
        )

        if len(text) > 4096:
            text = text[:4000] + "\n\n... (too many commits)"

        await msg.edit(text, disable_web_page_preview=True)

        # Pull updates
        subprocess.run(["git", "stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "pull", "origin", BRANCH], check=True)

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
