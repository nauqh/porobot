"""Embed factory

This module creates hikari embed for displaying on Discord.

"""
import hikari
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_patch_notes(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="html.parser")
        banner = soup.find('img')['src']
        summary = soup.find(
            'span', attrs={'class': 'content-border'}).find('img')['src']
    else:
        raise requests.HTTPError("Patch is not available")
    return banner, summary


def patch_embed(version: str, url: str) -> hikari.Embed:
    banner, summary = get_patch_notes(url)
    embed = (
        hikari.Embed(
            title=f"📝 Patch {version.replace('-', '.')} notes",
            description="**Author**: `Riot Riru`",
            colour="#9bf6ff",
            url=url
        )
        .add_field("View patch details", url)
        .set_image(summary)
        .set_thumbnail(banner)
    )
    return embed


def display_champs(champs: list) -> str:
    display = ""
    for champ in champs:
        display += (
            f"`{champ['name']}` **KDA** {champ['kda']}\n"
            f"**Matches**: {champ['matches_played']} **CS**: {champ['cs_rate']} **WR**: {champ['winrate']}%\n\n"
        )
    return display


def profile_embed(summoner, rank, region, url, champs, name, tag) -> hikari.Embed:
    if not rank:
        text = "**Unranked**"
    else:
        parts = rank['queueType'].split('_')
        queue_type = ' '.join([part.capitalize() for part in parts[:2]])

        text = (f"**{rank['tier'].capitalize()} {rank['rank']}**\n"
                f"{rank['wins']}W {rank['losses']}L {rank['leaguePoints']}LP\n\n"
                f"🕹️ **Live game**\n"
                f"Not curently playing")
    embed = (
        hikari.Embed(
            title=f"✨ {name} #{tag}",
            colour="#9bf6ff",
            description=f"**Champion pool**: {', '.join([champ['name'] for champ in champs])}",
            url=url,
            timestamp=datetime.now().astimezone()
        )
        .add_field(
            "📑 Info",
            (f"Level: {summoner['summonerLevel']}\n"
             f"Region: {region.upper()}\n"
             f"Winrate: {rank['wins']*100/(rank['wins']+rank['losses']):.1f}%"),
            inline=False
        )
        .add_field(
            f"🏆 {queue_type}",
            text,
            inline=True
        )
        .add_field(
            "⚔️ Champions",
            display_champs(champs),
            inline=True
        )
        .set_thumbnail(f"https://ddragon.leagueoflegends.com/cdn/13.23.1/img/profileicon/{summoner['profileIconId']}.png")
        .set_image(f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champs[0]['name'].replace(' ', '')}_0.jpg")
    )
    return embed


def build_embed(champion, header,  url,  runes, items):
    emojis = {
        "Inspiration": "💎",
        "Sorcery": "🔮",
        "Resolve": "🌲",
        "Domination": "🥊",
        "Precision": "✨"
    }

    keys = list(runes.keys())

    embed = (
        hikari.Embed(
            title=f"{header}",
            colour="#9bf6ff",
            description="Recommended runes and items",
            url=url,
            timestamp=datetime.now().astimezone()
        )
        .add_field(
            f"{emojis[keys[0]]} {keys[0]}",
            (f"{runes[keys[0]][0]}\n"
             f"{runes[keys[0]][1]}\n"
             f"{runes[keys[0]][2]}\n"
             f"{runes[keys[0]][3]}\n"),
            inline=True
        )
        .add_field(
            f"{emojis[keys[1]]} {keys[1]}",
            (f"{runes[keys[1]][0]}\n"
             f"{runes[keys[1]][1]}\n"),
            inline=True
        )
        .add_field(
            f"🔎 Items",
            (f"**Starter**: {', '.join(items[0])}\n"
             f"**Boot**: {', '.join(items[1])}\n"
             f"**Items**: {', '.join(items[2])}\n"),
            inline=False
        )
        .set_image(f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion.title().replace(' ', '')}_0.jpg")
        .set_thumbnail(f"https://ddragon.leagueoflegends.com/cdn/14.4.1/img/champion/{champion.title().replace(' ', '')}.png"))

    return embed
