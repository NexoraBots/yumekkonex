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
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


REPO_URL = "https://github.com/NexoraBots/yumekkonex"
BRANCH = "master"


@app.on_message(filters.command("update", prefixes=config.COMMAND_PREFIXES) & filters.user(config.OWNER_ID))
@error
@save
async def git_check_updates(client, message):

    msg = await message.reply("🔍 **Checking for updates...**")

    try:

        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)

        subprocess.run(["git", "fetch", "origin"], check=True)

        check_updates = subprocess.run(
            ["git", "rev-list", f"HEAD..origin/{BRANCH}", "--count"],
            capture_output=True,
            text=True
        )

        if check_updates.stdout.strip() == "0":
            return await msg.edit("✅ **Repository is already up to date.**")

        commits = subprocess.run(
            ["git", "log", f"HEAD..origin/{BRANCH}", "--pretty=format:%h|%an|%s|%ct"],
            capture_output=True,
            text=True
        )

        repo_link = REPO_URL.replace(".git", "")
        updates = ""

        for i, line in enumerate(commits.stdout.splitlines(), start=1):

            try:
                sha, author, summary, timestamp = line.split("|")
                date = datetime.fromtimestamp(int(timestamp)).strftime("%d %b %Y")

                updates += (
                    f"**➣ #{i}**: [{summary}]({repo_link}/commit/{sha})\n"
                    f"👤 **Author:** {author}\n"
                    f"📅 **Date:** {date}\n\n"
                )

            except:
                continue

        text = (
            "**🚀 Updates Available!**\n\n"
            "**📜 New Commits:**\n\n"
            f"{updates}\n"
            "⚡ **Do you want to update now?**"
        )

        if len(text) > 4096:
            text = text[:4000] + "\n\n..."

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✅ Update", callback_data="confirm_update"),
                    InlineKeyboardButton("❌ Cancel", callback_data="cancel_update"),
                ]
            ]
        )

        await msg.edit(text, reply_markup=buttons, disable_web_page_preview=True)

    except Exception as e:
        await msg.edit(f"❌ **Update check failed:**\n`{e}`")


@app.on_callback_query(filters.regex("confirm_update") & filters.user(config.OWNER_ID))
async def confirm_update(client, query):

    await query.answer()

    msg = await query.message.edit("⬇️ **Updating repository...**")

    try:

        subprocess.run(["git", "stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        subprocess.run(
            ["git", "reset", "--hard", f"origin/{BRANCH}"],
            check=True
        )

        if os.path.exists("requirements.txt"):
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
            )

        restart_message = await msg.edit(
            "✅ **Update successful!**\n\n🔁 **Restarting Yumeko...**"
        )

        save_restart_data(restart_message.chat.id, restart_message.id)

        await restart_bot()

    except Exception as e:
        await msg.edit(f"❌ **Update failed:**\n`{e}`")


@app.on_callback_query(filters.regex("cancel_update") & filters.user(config.OWNER_ID))
async def cancel_update(client, query):

    await query.answer("Update cancelled")

    await query.message.edit(
        "❌ **Update cancelled by owner.**"
    )


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
