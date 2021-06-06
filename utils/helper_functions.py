from api.gogoanimeapi import gogoanime as gogo
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import goth
from utils import formating_results as format

async def send_details(message, id):
    if 'split:' in id:
        split_id = id.split(":")
        x = gogo.get_search_results(split_id[1])
        (names, ids) = format.format_search_results(x)
        for i in ids:
            if i[-25:] == split_id[2]:
                id = i
                break
    search_details = gogo.get_anime_details(id)
    genre = search_details.get('genre')
    x = ''
    for i in genre:
        if i == "'" or i == "[" or i == "]":
            pass
        else:
            x = f'{x}{i}'
    await message.edit('Search Results:')
    try:
        try:
            await message.reply_document(
                f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
                document=search_details.get('image_url'),
                reply_markup=InlineKeyboardMarkup
                [
                    [
                        InlineKeyboardButton(
                    text="Download", callback_data=f"Download:{id}:{search_details.get('episodes')}")
                    ]
                ]
            )
        except:
            await message.reply(
                f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
                reply_markup=InlineKeyboardMarkup
                [
                    [
                        InlineKeyboardButton(
                    text="Download", callback_data=f"Download:{id}:{search_details.get('episodes')}")
                    ]
                ]
            )
    except:
        try:
            await message.reply_document(
                f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeID: `{id}`",
                document=search_details.get('image_url'),
                reply_markup=InlineKeyboardMarkup
                [
                    [
                        InlineKeyboardButton(
                    text="Download", callback_data=f"longdl:{split_id[1]}:{id[-25:]}:{search_details.get('episodes')}")
                    ]
                ]
            )
        except:
            await message.reply_document(
                f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
                document=search_details.get('image_url'),
                reply_markup=InlineKeyboardMarkup
                [
                    [
                        InlineKeyboardMarkup(text="Download", callback_data=f"longdl:{split_id[1]}:{id[-25:]}:{search_details.get('episodes')}")
                    ]
                ]
            )
            
async def send_download_link(message, id, ep_num):
    links = gogo.get_episodes_link(animeid=id, episode_num=ep_num)
    result = format.format_download_results(links)
    if "status" in result:
        return False
    else:
        await message.reply(
            f"Download Links for episode {ep_num}\n{result}"
        )
        
    return True