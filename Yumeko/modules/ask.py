import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Yumeko import app
from config import config
from Yumeko.decorator.save import save
from Yumeko.decorator.errors import error
import httpx

NVIDIA_AI_KEY = "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"
NVIDIA_API_URL = "https://api.nvidia.ai/v1/chat/completions"

@app.on_message(filters.command("ask", config.COMMAND_PREFIXES))
@error
@save
async def ask_nvidia(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/ask <your question>`", quote=True)
        return

    prompt = message.text.split(maxsplit=1)[1]
    processing_message = await message.reply_text("💭 Thinking... Please wait.", quote=True)

    try:
        # Call NVIDIA AI API
        async with httpx.AsyncClient(timeout=60) as session:
            payload = {
                "model": "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",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
            headers = {"Authorization": f"Bearer {NVIDIA_AI_KEY}"}
            response = await session.post(NVIDIA_API_URL, json=payload, headers=headers)
            response_data = response.json()

        # Extract AI response
        answer = response_data.get("choices", [{}])[0].get("message", {}).get("content")
        if not answer:
            answer = "I couldn't generate a response. Please try again."

        await processing_message.edit_text(f"**Prompt:** {prompt}\n\n**Response:** {answer}")

    except Exception as e:
        await processing_message.edit_text(f"An error occurred: {e}")
        
__module__ = "𝖠𝗌𝗄"
__help__ = """✧ /ask <prompt> : 𝖴𝗌𝖾 𝖦𝖯𝖳-3.5-𝗍𝗎𝗋𝖻𝗈 𝗍𝗈 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗋𝖾𝗌𝗉𝗈𝗇𝗌𝖾𝗌."""
