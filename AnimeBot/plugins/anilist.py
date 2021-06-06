import json
import asyncio
import requests
from AnimeBot import goth, cmd
from utils.errors import capture_err
from api.anilistapi import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@goth.on_message(cmd(["airing", "airing@AnimeGothBot"]))
@capture_err
async def anime_airing(_, message):
    search_str = message.text.split(' ', 1)
    if len(search_str) == 1:
        await message.reply_text('Provide anime name!')
        return
    variables = {'search': search_str[1]}
    response = requests.post(
        url, json={'query': airing_query, 'variables': variables}).json()['data']['Media']
    ms_g = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response['nextAiringEpisode']:
        airing_time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
        airing_time_final = t(airing_time)
        ms_g += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`"
    else:
        ms_g += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await message.reply_text(ms_g)

    
@goth.on_message(cmd(["animeinfo", "animeinfo@AnimeGothBot"]))
@capture_err
async def anime_search(_, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    else:
        search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={'query': anime_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    if json:
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '`\n'
        msg += "**Studios**: `"
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get(
            'description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
        msg += shorten(description, info)
        image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
        if trailer:
            buttons = [
                    [InlineKeyboardButton("More Info", url=info),
                    InlineKeyboardButton("Trailer 🎬", url=trailer)]
                    ]
        else:
            buttons = [
                    [InlineKeyboardButton("More Info", url=info)]
                    ]
        if image:
            try:
                await message.reply_photo(image, caption=msg, reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [〽️]({image})"
                await message.edit(msg)
        else:
            await message.edit(msg)
 
   
@goth.on_message(cmd(["mangainfo", "mangainfo@AnimeGothBot"]))
@capture_err
async def manga_search(_, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={'query': manga_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    ms_g = ''
    if json:
        title, title_native = json['title'].get(
            'romaji', False), json['title'].get('native', False)
        start_date, status, score = json['startDate'].get('year', False), json.get(
            'status', False), json.get('averageScore', False)
        if title:
            ms_g += f"**{title}**"
            if title_native:
                ms_g += f"(`{title_native}`)"
        if start_date:
            ms_g += f"\n**Start Date** - `{start_date}`"
        if status:
            ms_g += f"\n**Status** - `{status}`"
        if score:
            ms_g += f"\n**Score** - `{score}`"
        ms_g += '\n**Genres** - '
        for x in json.get('genres', []):
            ms_g += f"{x}, "
        ms_g = ms_g[:-2]

        image = json.get("bannerImage", False)
        ms_g += f"_{json.get('description', None)}_"
        if image:
            try:
                await message.reply_photo(image, caption=ms_g)
            except:
                ms_g += f" [〽️]({image})"
                await message.reply(ms_g)
        else:
            await message.reply(ms_g)


@goth.on_message(cmd(["character", "character@AnimeGothBot"]))
@capture_err
async def character_search(_, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    search = search[1]
    variables = {'query': search}
    json = requests.post(url, json={'query': character_query, 'variables': variables}).json()[
        'data'].get('Character', None)
    if json:
        ms_g = f"**{json.get('name').get('full')}**(`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        ms_g += shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            await message.reply_photo(image, caption=ms_g)
        else:
            await message.reply(ms_g)
            
@goth.on_message(cmd(["top", f"top@AnimeGothBot"]))
async def top_tags_cmd(_, message):
    query = message.text.split(" ", 1)
    get_tag = "None"
    if len(query)==2:
        get_tag = query[1]
    user = message.from_user.id
    result = await get_top_animes(get_tag, 1, user)
    if len(result) == 1:
        await message.reply_text(result[0])
    msg, buttons = result
    await goth.send_message(message.chat.id, msg, reply_markup=buttons)
