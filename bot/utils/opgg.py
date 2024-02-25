from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import quote


def get_champions(summoner, tag):
    url = f"https://www.op.gg/summoners/vn/{quote(summoner)}-{tag}"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    champions = soup.find_all('div', attrs={'class': 'champion-box'})

    infos = []
    for champion in champions:
        info = {}

        # Extracting champion name
        info['name'] = champion.find(
            'div', class_='name').text.strip()

        # Extracting KDA
        kda_text = champion.find('div', class_='kda').text.strip()
        kda = kda_text.split(' ')[0]
        info['kda'] = kda

        # Extracting winrate
        winrate_text = champion.find('div', class_='played').text.strip()
        winrate = winrate_text.split('%')[0]
        info['winrate'] = winrate

        # Extracting number of matches played
        matches_text = champion.find('div', class_='count').text.strip()
        matches = matches_text.split(' ')[0]
        info['matches_played'] = matches

        # Extracting CS rate
        cs_text = champion.find('div', class_='cs').text.strip()
        cs_rate = cs_text.split(' ')[2][1:-1]
        info['cs_rate'] = cs_rate

        infos.append(info)
    return infos


def get_runes(name: str):
    url = f"https://www.op.gg/champions/{name.replace(' ', '')}/build?region=kr"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    header = soup.find('h1').text

    try:
        builds = []
        source = []
        for item in soup.find_all('span', {"class": "css-1h6ea4y e1y8mv8s2"}):
            source.append(item.text)

        boards = soup.find_all("div", {"class": "css-1l6y0w9 e1y8mv8s0"})
        for board in boards:
            build = []
            rows = board.find_all("div", {"class": "row"})
            for row in rows:
                element = row.find('div', {"class": "css-1k1cq3m"})
                if element is not None:
                    build.append(element.find('img')['alt'])
            builds.append(build)
        builds[0].insert(0, soup.find(
            'div', {"class": 'css-19js88b e1y8mv8s1'}).find('img')['alt'])

        return header, url, {source[i]: builds[i] for i in range(2)}
    except Exception:
        return None


def get_items(champion: str):
    """
    tbody:
        0: Starter items
        1: Boots
        2: Recommended Builds
    """
    url = f"https://www.op.gg/champions/{champion.replace(' ', '')}/build?region=kr"
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    items = []
    for mode in range(3):
        tr_tags = soup.find_all("tbody")[mode].find_all("tr")
        items_mode = []
        for tr_tag in tr_tags:
            imgs = tr_tag.find_all('img')
            bag = [img['alt'] for img in imgs]
            items_mode.append(bag)
        items.append(items_mode[0])
    return items
