from AnimeBot import goth, cmd
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api.gogoanimeapi import gogoanime as gogo
import utils.formating_results as format
from utils.helper_functions import *
from utils.errors import capture_err

@goth.on_message(cmd(["anime", "anime@AnimeGothBot"]))
@capture_err
async def anime(_, message):
    query = message.text.split(" ", 1)
    if len(query) == 1:
        await message.reply_text("Command must be used like this\n/anime [name of anime]\nexample: /anime One Punch Man")
        return
    else:
        query = query[1]
        search_result = gogo.get_search_results(query)
        try:
            (names, ids) = format.format_search_results(search_result)
            sed = []
            for i in range(len(names)):
                if len(names[i]) > 55:
                    try:
                        sed.append(
                            InlineKeyboardMarkup
                            [
                                [
                                    InlineKeyboardButton(text=f"{names[i][:22]}. . .{names[i][-22:]}", callback_data =f"split:{anime_name}:{ids[i][-25:]}")
                                ]
                            ]
                        )
                    except:
                        message.reply_text("Name too long")
                else:
                    sed.append(
                        InlineKeyboardMarkup
                        [
                            [
                                InlineKeyboardButton(text=f"{names[i]}", callback_data =f"dets:{ids[i]}")
                            ]
                        ]
                    )
            await message.reply("Search Results:", reply_markup=sed)
        except:
            await message.reply_text("No Results found! Try Japanese Names once!!")
        
@goth.on_message(cmd(["latest", "latest@AnimeGothBot"]))
@capture_err
async def latest(_, message):
    query = gogo.get_home_page()
    (names, ids, epnums) = format.format_home_results(query)
    inline = []
    for i in range(len(names)):
        try:
            inline.append(
                InlineKeyboardMarkup
                [
                    [
                        InlineKeyboardButton(text=f"{names[i]}", callback_data=f"lt:{ids[i]}")
                    ]
                ]
            )
        except:
            pass
    await goth.reply_text("**Latest Animes:**", reply_markup=inline, parse_mode="markdown")
    
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

    
@bot.on_message(cmd(["batch", "batch@AnimeGothBot"]))
@capture_err
async def batch(_, message):
    if message.chat.type != "private":
        await event.reply("If you want to download in batch contact me in pm", reply_markup=pm)
            return
        try:
            text = message.text.split(" ", 1)
            name = text[1]
            split_data = name.split(":")
            if int(split_data[2]) - int(split_data[1]) > 15:
                await message.reply(
                    "Batch Download is limited at 15 episodes due to performance issues\nPlease download in batches of less than 15 for now"
                )
            else:
                for i in range(int(split_data[1]), (int(split_data[2]) + 1)):
                    if await send_download_link(split_data[0], i) == False:
                        break
        except:
            await message.reply("Something Went Wrong\nCheck /help for proper use of this command!")
          
@goth.on_message(cmd(["download", "download@AnimeGothBot"]))
@capture_err
async def dl(_, message):
    try:
        text = message.text.split(" ", 1)
        anime_name = text[1]
        split_data = anime_name.split(":")
        if int(split_data[2]) - int(split_data[1]) > 100:
            await event.reply(
                    "Batch Download is limited at 100 episodes due to performance issues\nPlease download in batches of less than 100 for now"
            )
            return
        list_of_links = []
        await event.reply("Be Patient this is a slow process....")
        for i in range(int(split_data[1]), (int(split_data[2]) + 1)):
            list_of_links.append(gogo.get_episodes_link(split_data[0], i))
        format.batch_download_txt(split_data[0], list_of_links)
        await goth.send_document(
                message.chat_id,
                "Import this file in **1DM** app.",
                document=f"{split_data[0]}.txt"

            )
        except:
            await message.reply("Something Went Wrong\nCheck /help for proper use of this command!")
            
#CallBackQueries...

@goth.on_callback_query(filters.regex("lt:"))
async def callback_latest(_, CallBackQuery):
    data = CallBackQuery.data
    split_data = data.split(":")
    animeid = split_data[-1]
    await send_details(animeid)
    
@goth.on_callback_query(filters.regex("Download"))
async def callback_for_download(_, CallBackQuery):
    data = CallBackQuery.data
    x = data.split(":")
    button2 = [[]]
    current_row = 0
    if int(x[2]) < 101:
        for i in range(int(x[2])):
            button2[current_row].append(InlineKeyboardButton(
                str(i+1), callback_data=f'ep:{i+1}:{x[1]}'))
            if (i+1) % 5 == 0:
                button2.append([])
                current_row = current_row + 1
        await CallBackQuery.edit(
            reply_markup=InlineKeyboardMarkup(button2)
        )
    else:
        num_of_buttons = (int(x[2]) // 100)
        for i in range(num_of_buttons):
            button2[current_row].append(InlineKeyboardButton(
                f'{i}01 - {i+1}00', callback_data=f'btz:{i+1}00:{x[1]}'))
            if (i+1) % 3 == 0:
                button2.append([])
                current_row = current_row + 1
        if int(x[2]) % 100 == 0:
            pass
        else:
            button2[current_row].append(InlineKeyboardButton(
                f'{num_of_buttons}01 - {x[2]}', data=f'etz:{x[2]}:{x[1]}'))
        await CallBackQuery.edit(
            reply_markup=InlineKeyboardMarkup(button2)
        )
        
@goth.on_callback_query(filters.regex("longdl"))
async def callback_for_download_long(_, CallBackQuery):
    data = CallBackQuery.data
    x = data.split(":")
    button2 = [[]]
    current_row = 0
    search_results = gogo.get_search_results(x[1])
    (names, ids) = format.format_search_results(search_results)
    for i in ids:
        if i[-25:] == x[2]:
            id = i
            break
    for i in range(int(x[3])):
        button2[current_row].append(InlineKeyboardButton(
            str(i+1), data=f'spp:{i+1}:{x[2]}:{x[1]}'))
        if (i+1) % 5 == 0:
            button2.append([])
            current_row = current_row + 1
    await CallBackQuery.edit(
        f'Choose Episode:',
        reply_markup=InlineKeyboardMarkup(button2)
    )
    
@goth.on_callback_query(filters.regex("btz:"))
async def callback_for_choosebuttons(_, CallBackQuery):
    data = CallBackQuery.data
    data_split = data.split(':')
    button3 = [[]]
    current_row = 0
    endnum = data_split[1]
    startnum = int(f'{int(endnum[0])-1}01')
    for i in range(startnum, (int(endnum)+1)):
        button3[current_row].append(InlineKeyboardButton(
            str(i), callback_data=f'ep:{i}:{data_split[2]}'))
        if i % 5 == 0:
            button3.append([])
            current_row = current_row + 1
    await CallBackQuery.edit(
            reply_markup=InlineKeyboardMarkup(button3)
    )
    
@goth.on_callback_query(filters.regex("ep:"))
async def callback_for_downlink(_, CallBackQuery):
    data = CallBackQuery.data
    try:
        data_split = data.split(':')
        await send_download_link(data_split[2], data_split[1])
    except:
        pass
    
@goth.on_callback_query(filters.regex("spp:"))
async def callback_for_downlink_long(_, CallBackQuery):
    data = CallBackQuery.data
    x = data.split(":")
    search_results = gogo.get_search_results(x[3])
    (names, ids) = format.format_search_results(search_results)
    for i in ids:
        if i[-25:] == x[2]:
            id = i
            break
    await send_download_link(id, x[1])
    
@goth.on_callback_query(filters.regex("dets:"))
async def callback_for_details(_, CallBackQuery):
    data = CallBackQuery.data
    x = data.split(":")
    await send_details(x[1])

@goth.on_callback_query(filters.regex("split:"))
async def callback_for_details_long(_, CallBackQuery):
    data = CallBackQuery.data
    await send_details(data)
