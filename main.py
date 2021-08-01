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
Hello {}, ⬇️ ** I am Telegraph Uploader Bot**

`I Can Uploade telegra.ph . Just send me some Image , Video 'size 5MB below', and see magic.`

**🙋 Maintained By:** ▷ @DHKBots 🤖
"""
ABOUT_TEXT = """
- **Bot :** `Telegraph Uploader`
- **Channel :** [DHK BOTS]
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('About', callback_data='About'),
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel',url='https://telegram.me/DHKBots')
        ]]
    )

@tgraph.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    

@tgraph.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
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
     
    
@tgraph.on_message(filters.media)
async def getmedia(client, message):
    dwn = await message.reply_text("Downloading to my server...", True)
    media_path = await message.download()
    await dwn.edit_text("Uploading as telegra.ph link...")
    try:
        url_path = upload_file(media_path)[0]
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{url_path}</code>",
    )
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        text=f"Error :- <code>{error}</code>"
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('More Help', callback_data='help')
            ]]
        )
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        return
    text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>Join :-</b> @DHKBots"
    reply_markup=InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{url_path}"),
        InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{url_path}")
        ],[
        InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/DHKBots")
        ]]
    )
    await message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    try:
        os.remove(medianame)
    except:
        pass

tgraph.run()
