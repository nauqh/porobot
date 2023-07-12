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


if __name__ == "__main__":
    champion = "brands"
    rows = runes(champion)
    print(rows)

    # items = build(champion, 3)
    # print(items)

# @plugin.command
# @lightbulb.option(
#     "champion", "The champion to get information about.", required=True
# )
# @lightbulb.command(
#     "get", "Get info about the champion.", auto_defer=True
# )
# @lightbulb.implements(lightbulb.SlashCommand)
# async def get(ctx: lightbulb.Context):
#     champion = ctx.options.champion

#     # TODO: VALIDATE
#     error = runes(champion)
#     if error == None:
#         await ctx.respond(f"No champion name `{champion}`, try again")
#     else:
#         # TODO: RUNES
#         primary = []
#         rows = runes(champion)['primary']
#         for row in rows:
#             primary.append(get_main_rune(row))

#         secondary = []
#         rows = runes(champion)['secondary']
#         for row in rows:
#             if get_main_rune(row) == None:
#                 secondary.append("_")
#             else:
#                 secondary.append(get_main_rune(row))

#         # TODO: ITEMS
#         items = build(champion, 3)

#         embed = (
#             hikari.Embed(
#                 title=f"**{champion.capitalize()}** Build",
#                 description=f"**Branch**: `{primary[1]}`",
#                 colour=0x9bf6ff,
#                 timestamp=datetime.now().astimezone(),
#                 url=f"https://www.op.gg/modes/aram/{champion}/build?region=kr"
#             )
#             .set_thumbnail(f"http://ddragon.leagueoflegends.com/cdn/13.13.1/img/champion/{champion.capitalize()}.png")
#             .add_field(
#                 primary[2],
#                 secondary[1],
#                 inline=True
#             )
#             .add_field(
#                 primary[3],
#                 secondary[2],
#                 inline=True
#             )
#             .add_field(
#                 primary[4],
#                 secondary[3],
#                 inline=True
#             )
#             .add_field(
#                 "**Items**",
#                 ', '.join(items[0]),
#                 inline=False
#             )
#             .add_field(
#                 "**Alternatives**",
#                 ', '.join(items[1]),
#                 inline=True
#             )
#             .set_footer(
#                 text=f"Requested by {ctx.member.display_name}",
#                 icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
#             )
#         )

#         await ctx.respond(embed)
