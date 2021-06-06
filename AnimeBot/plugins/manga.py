from AnimeBot import goth, cmd
from pyrogram import filters
from api.kissmangaapi import kissmangaapi as kiss
from utils.helper_functions import *
import utils.formating_results as format
from utils.errors import capture_err

@goth.on_message(cmd(["manga", "manga@AnimeGothBot"]))
@capture_err
async def manga(_, message):
    query = message.text.split(" ", 1)
    if len(query) == 1:
        await message.reply_text("Command must be used like this\n/manga [name of manga]\nexample: /manga One Punch Man")
    else:
        query = query[1]
        results = kiss.get_search_results(query)
        if len(results) == 0:
            message.reply_text("No Results found! Try Japanese Names once!!")
        else:
            try:
                inline = []
                for i in results:
                    inline.append(
                        InlineKeyboardMarkup
                        [
                            [
                                InlineKeyboardButton(text=f"{i[0]}", callback_data=f"mid:{i[1]}")
                            ]
                        ]
                    )
                await message.reply_text("Search Results:", reply_markup=inline)
            except:
                pass

           
@goth.on_message(cmd(["read", "read@AnimeGothBot"]))
@capture_err
async def read(_, message):
    try:
        data = message.text.split(" ", 1)
        if len(data) == 1:
            await message.reply_text("Something Went Wrong! Check /help for proper usage!")
            return
        else:
            data = data[1]
            query = data.split(":")
            chap = kiss.get_manga_chapter(query[0], query[1])
            if chap == "Invalid Mangaid or chapter number":
                await message.reply_text("Something Went Wrong! Check /help for proper usage!")
                return
            format.manga_chapter_html(f"{data[0]}{data[1]}", chap)
            await message.reply("Open This in a Browser", document=f"{split_data[0]}{split_data[1]}.html")
    except Exception as e:
            await message.reply({e})
            
@goth.on_callback_query(filters.regex("mid:"))
async def callback_mangaxtra(_, CallBackQuery):
    data = CallBackQuery.data
    xtra = kiss.get_manga_details(data[4:])
    await message.reply_document(f"Name: {xtra[0]}\nGenre: {', '.join(xtra[2])}\nLatest Chapter: {xtra[3]}\n\n\nCopy This command and add chapter number at end\n\n`/read {data[4:]}:`", document=xtra[1])