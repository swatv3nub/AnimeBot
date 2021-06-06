from AnimeBot import telegraph
import requests

def nhentai(awoos):
    url = f"https://nhentai.net/api/gallery/{awoos}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res['num_pages']
    extensions = {
        'j':'jpg',
        'p':'png',
        'g':'gif'
    }
    for i, x in enumerate(pages):
        media_id = res["media_id"]
        temp = x['t']
        file = f"{i+1}.{extensions[temp]}"
        link = f"https://i.nhentai.net/galleries/{media_id}/{file}"
        links.append(link)

    for i in info:
        if i["type"]=="tag":
            tag = i['name']
            tag = tag.split(" ")
            tag = "_".join(tag)
            tags+=f"#{tag} "
        if i["type"]=="artist":
            artist=f"{i['name']} "

    post_content = "".join(f"<img src={link}><br>" for link in links)

    post = telegraph.create_page(
        f"{title}",
        html_content=post_content,
        author_name=f"AnimeGothBot", 
        author_url=f"https://t.me/AnimeGothBot"
    )
    return title,tags,artist,total_pages,post['url'],links[0]