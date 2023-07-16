from urllib import request
from bs4 import BeautifulSoup


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


if __name__ == "__main__":
    champion = "kaisa"
    r = runes(champion)
    print(r['primary'][1])

    items = build(champion, 3)
    print(items)
