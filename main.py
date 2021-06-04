import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.WARNING)


tgraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH
)


START_TEXT = """
Hello {}, I am Telegraph Image uplod-bot or file to telegra.ph link uploader bot.

Made by @umeshnamo
"""
HELP_TEXT = """
- Just give me a Image
- Then I will download it
- I will then upload it to the telegra.ph link

Made by @umeshnamo
"""
ABOUT_TEXT = """
- **Bot :** `Telegraph Uploader`
- **Creator :** [DHK BOSS](https://telegram.me/umeshnamo)
- **Channel :** [DHK BOTS](https://telegram.me/DHKBots)
    )


@tgraph.on_message(filters.photo)
async def getimage(client, message):
    dwn = await message.reply_text("Downloading to my server...", True)
    img_path = await message.download()
    await dwn.edit_text("Uploading as telegra.ph link...")
    try:
        url_path = upload_file(img_path)[0]
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{url_path}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open Link", url=f"https://telegra.ph{url_path}"
                    ),
                    InlineKeyboardButton(
                        text="Share Link",
                        url=f"https://telegram.me/share/url?url=https://telegra.ph{url_path}",
                    )
                ]
            ]
        )
    )
    os.remove(img_path)


tgraph.run()
