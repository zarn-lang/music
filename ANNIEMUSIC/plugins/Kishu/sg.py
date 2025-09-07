import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from ANNIEMUSIC import userbot as us, app
from ANNIEMUSIC.core.userbot import assistants


@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    if not assistants or 1 not in assistants:
        return await message.reply("❌ No active userbot assistant found!")

    ubot = us.one
    status_msg = await message.reply("👀")

    try:
        if message.reply_to_message:
            target_user_id = message.reply_to_message.from_user.id
        else:
            parts = message.text.split()
            if len(parts) < 2:
                return await status_msg.edit("❌ Usage: `/sg` username / id / reply", parse_mode="MARKDOWN")
            target_user_id = parts[1]

        user = await client.get_users(target_user_id)
    except Exception as e:
        return await status_msg.edit("❌ Invalid user. Please reply to a user or provide a valid username/id.")

    sangmata_bots = ["sangmata_bot", "sangmata_beta_bot"]
    sg_bot = random.choice(sangmata_bots)

    try:
        forward_msg = await ubot.send_message(sg_bot, str(user.id))
        await forward_msg.delete()
    except Exception as e:
        return await status_msg.edit(f"❌ Failed to contact @`{sg_bot}`\n`{e}`", parse_mode="MARKDOWN")

    await asyncio.sleep(1.5)

    found = False
    async for stalk in ubot.search_messages(sg_bot):
        if stalk and stalk.text:
            await message.reply(stalk.text)
            found = True
            break

    if not found:
        await message.reply("🤖 Bot didn't return any username history.")

    try:
        peer = await ubot.resolve_peer(sg_bot)
        await ubot.send(DeleteHistory(peer=peer, max_id=0, revoke=True))
    except Exception:
        pass

    await status_msg.delete()
