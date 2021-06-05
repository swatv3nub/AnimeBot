from AnimeBot import goth, cmd
from api.nhentaiapi import nhentai as nh
from utils.errors import capture_err

@goth.on_message(cmd(["nhentai", "nhentai@AnimeGothBot"]))
@capture_err
async def nhentai(client, message):
    query = message.text.split(" ")[1]
    title, tags, artist, total_pages, post_url, cover_image = nh(query)
    await message.reply_text(
        f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Read Here",
                        url=post_url
                    )
                ]
            ]
        )
    )
