from pyrogram import filters
import builtins
import time

app = builtins.app

@app.on_message(filters.command("ping", prefixes="/") & filters.me)
async def ping(client, message):
    start_time = time.time()
    msg = await message.reply_text("🏓 Pong...")
    end_time = time.time()
    latency = int((end_time - start_time) * 1000)
    await msg.edit_text(f"🏓 Pong! `{latency}ms`")