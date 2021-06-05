from AnimeBot import goth, cmd
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.strings import start_text, help_text

photo = "https://telegra.ph/file/0f89bae1e77ca43f81f78.jpg"

pm = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Contact Me in PM!",
                        url="t.me/AnimeGothBot?start",
                    )
                ]
            ]
        )

@goth.on_message(cmd(["start", "start@AnimeGothBot"]))
async def start(_, message):
    if message.chat.type == "private":
        await message.reply_photo(photo, caption=start_text, parse_mode="markdown")
        return
    else:
        await message.reply_text("Hello {mention}, I am an fully Equiped Anime Bot. Try /help to check my Features!")
        return
        
@goth.on_message(cmd(["help", "help@AnimeGothBot"]))
async def helper(_, message):
    if message.chat.type == "private":
        await message.reply_text(help_text, parse_mode="markdown")
        return
    else:
        await message.reply_text("PM me for more info!", reply_markup=pm)
        return
    
@goth.on_message(cmd(["source", "source@AnimeGothBot"]))
async def source(_, message):
    await message.reply_text(
        "Source Code On [Github](https://github.com/swatv3nub/AnimeBot)\nHosted in Heroku, Please don't Abuse", disable_web_page_preview=True
    )
    return

