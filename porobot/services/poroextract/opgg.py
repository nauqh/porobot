from urllib import request
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from requests import get


def build(champion_name: str, mode: int):
    """
    tbody:
        0: Tier list
        1: Starter items
        2: Boots
        3: Recommended Builds
    """
    url = f"https://www.op.gg/modes/aram/{champion_name}/build?region=kr"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    tr_tags = soup.find_all("tbody")[mode].find_all("tr")

    items = []
    for tr_tag in tr_tags:
        imgs = tr_tag.find_all('img')
        bag = [img['alt'] for img in imgs]
        items.append(bag)
    return items


def runes(champion_name: str):
    """
    Return:
        keys (primary, secondary, side): list of rows
    """
    # TODO: Extract data
    url = f"https://www.op.gg/modes/aram/{champion_name}/build?region=kr&hl=en_US"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    error = soup.find_all("div", {"class": "title"})
    if error:
        return None
    else:
        tables = soup.find_all(
            "div", {"class": "css-18v97ez e1jxk9el3"})[0].find_all("div", recursive=False)
        # only use table 0, 2, 4; (1, 3 are dividers)
        tables = [table for i, table in enumerate(tables) if i % 2 == 0]

        # TODO: Store as dict
        keys = ["primary", "secondary", "side"]
        values = []
        for table in tables:
            rows = table.find_all("div", {"class": "row"})
            imgs = []
            for row in rows:
                imgs.append(row.find_all("img"))
            values.append(imgs)

        return {keys[i]: values[i] for i in range(len(keys))}


def to_dict(img_tag: str):
    soup = BeautifulSoup(img_tag, 'html.parser')
    attributes = ['alt', 'src', 'height', 'width']
    dictionary = {attr: soup.img.get(attr)
                  for attr in attributes if soup.img.get(attr)}
    return dictionary


def get_main_rune(img_tags):
    for img_tag in img_tags:
        img_tag = str(img_tag)
        soup = BeautifulSoup(img_tag, 'html.parser')
        if 'grayscale' not in soup.img.get('src', ''):
            return to_dict(img_tag)['alt']


def get_profile(summoner: str, region: str):
    url = f"https://www.op.gg/summoners/{region}/{summoner.replace(' ', '%20')}"

    session = HTMLSession()
    soup = BeautifulSoup(session.get(url).html.raw_html, features='lxml')

    profile = {
        'name': summoner,
        'region': region,
        'url': url,
        'avatar': soup.select_one("div.profile-icon img")['src'],
        'level': soup.select_one("div.profile-icon img").find_next_sibling().text
    }

    try:
        champs = [{
            'name': champ.find("div", {"class": "name"}).text,
            'kda': champ.find("div", {"class": "css-954ezp e1g7spwk1"}).text,
            'winrate': champ.find("div", {"class": "css-1nuoroq e1g7spwk0"}).text
        } for champ in soup.find_all("div", {"class": "champion-box"})[:3]]
    except Exception:
        champs = {}

    try:
        rank = {
            'tier': soup.select_one('div.content:nth-child(2) .tier').text,
            'lp': soup.select_one('div.content:nth-child(2) .lp').text,
            'win_lose': soup.select_one('div.content:nth-child(2) .win-lose').text,
            'ratio': soup.select_one('div.content:nth-child(2) .ratio').text
        }
    except Exception:
        rank = {}

    return profile, champs, rank


def get_rotation(api_key="RGAPI-a384a673-d288-42ec-a860-55a1602dba94"):
    rotation = get(
        f"https://vn2.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api_key}").json()

    patch = get(
        "https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    champions = get(
        f"http://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json").json()['data']
    champ_ids = rotation['freeChampionIds']

    names = []
    for name in champions:
        if int(champions[name]['key']) in champ_ids:
            names.append(name)

    return names
