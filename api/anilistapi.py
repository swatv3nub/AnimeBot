import math
import time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests

def shorten(description, info='anilist.co'):
    ms_g = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        ms_g += f"\n**Description**: __{description}__[Read More]({info})"
    else:
        ms_g += f"\n**Description**: __{description}__"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )


def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]
    
async def return_json(query: str, vars: dict, user: int = None):
    response = requests.post(url, json={"query": query, "variables": vars}).json()
    return response

    
async def get_top_animes(gnr: str, page, user):
    vars_ = {"gnr": gnr.lower(), "page": int(page)}
    query = top_query
    if gnr=="None":
        query = alltop_query
        vars_ = {"page": int(page)}
    result = await return_json(query, vars_, user=user)
    if len(result['data']['Page']['media'])==0:
        return [f"No results Found"]
    data = result["data"]["Page"]
    msg = f"Top animes for genre `{gnr.capitalize()}`"
    for i in data:
        msg += f"⚬ {i['media']['title']['romaji']}"
    btn = []
    if int(page)==1:
        if int(data['pageInfo']['lastPage'])!=1:
            btn.append([InlineKeyboardButton("Next", callback_data=f"topanimu_{gnr}_{int(page)+1}_{user}")])
    elif int(page) == int(data['pageInfo']['lastPage']):
        btn.append([InlineKeyboardButton("Prev", callback_data=f"topanimu_{gnr}_{int(page)-1}_{user}")])
    else:
        btn.append([
            InlineKeyboardButton("Prev", callback_data=f"topanimu_{gnr}_{int(page)-1}_{user}"),
            InlineKeyboardButton("Next", callback_data=f"topanimu_{gnr}_{int(page)+1}_{user}")
        ])
    return msg, InlineKeyboardMarkup(btn)


airing_query = '''
    query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        episodes
        title {
          romaji
          english
          native
        }
        siteUrl
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        } 
      }
    }
    '''

fav_query = """
query ($id: Int) { 
      Media (id: $id, type: ANIME) { 
        id
        title {
          romaji
          english
          native
        }
     }
}
"""

anime_query = '''
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        idMal
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''
character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               favourites
               image {
                        large
               }
               description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) { 
      Media (id: $id, type: MANGA,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""

top_query = """
query ($gnr: String, $page: Int) {
  Page (perPage: 15, page: $page) {
    pageInfo {
      lastPage
    }
    media (genre: $gnr, sort: SCORE_DESC, type: ANIME) {
      title {
        romaji
      }
    }
  }
}
"""

alltop_query = """
query ($page: Int) {
  Page (perPage: 15, page: $page) {
    pageInfo {
      lastPage
    }
    media (sort: SCORE_DESC, type: ANIME) {
      title {
        romaji
      }
    }
  }
}
"""


url = 'https://graphql.anilist.co'

