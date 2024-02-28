"""Embed factory

This module creates hikari embed for displaying on Discord.

"""
import hikari
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots


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
                f"NA")
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


def graph_dmgproportion(names, trues, physicals, magics):
    fig = go.Figure()

    damage_types = ['True Damage', 'Physical Damage', 'Magic Damage']
    colors = ['#ff9500', '#ffc300', '#ffdd00']

    for damage_type, color in zip(damage_types, colors):
        fig.add_trace(go.Bar(
            y=names,
            x=trues if damage_type == 'True Damage' else (
                physicals if damage_type == 'Physical Damage' else magics),
            name=damage_type,
            orientation='h',
            marker=dict(color=color),
            hovertemplate='%{x:,.0f}'
        ))

    fig.update_layout(title='Damage Proportion', barmode='stack', title_font_size=20,
                      title_font_color='#FAFAFA', height=450,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      legend=dict(orientation="h", yanchor="top", xanchor="center", x=0.5, y=1.1,
                                  font_color="#fafafa"))
    
    fig.update_yaxes(showgrid=False, title=None, tickfont=dict(color='#FAFAFA'))
    fig.update_xaxes(title=None, tickfont=dict(color='#FAFAFA'))
    fig.write_image("dmg_proportion.png")

def convert_timestamp_to_date(timestamp):
    date_object = datetime.utcfromtimestamp(timestamp)
    formatted_date = date_object.strftime('%b %d %H:%M')
    return formatted_date

def graph_personal(matchdf, playerdf):
    # Reverse the order of rows
    matchdf = matchdf.iloc[::-1].reset_index(drop=True)
    playerdf = playerdf.iloc[::-1].reset_index(drop=True)

    matchdf['CSperMin'] = (playerdf['totalMinionsKilled'] + playerdf['neutralMinionsKilled']) / \
        (matchdf['gameDuration'] / 60)
    matchdf['VisionperMin'] = playerdf['visionScore'] / \
        (matchdf['gameDuration'] / 60)
    matchdf['GoldperMin'] = playerdf['goldEarned'] / \
        (matchdf['gameDuration'] / 60)

    matchdf['gameCreation'] = matchdf['gameCreation'] / 1000
    matchdf['gameCreation'] = matchdf['gameCreation'].apply(
        convert_timestamp_to_date)

    # Calculate the difference between CSperMin and GoldperMin
    matchdf['CS_Gold_Difference'] = abs(
        matchdf['CSperMin'] - matchdf['GoldperMin'])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

   # Extract champion names
    champion_names = playerdf['championName']

    # Creating traces for VisionperMin
    vision_trace = go.Scatter(
        x=matchdf['gameCreation'],
        y=round(matchdf['VisionperMin'], 2),
        mode='lines+markers',
        name='VisionperMin',
        hovertemplate='%{y:.1f}'
    )

    # Creating traces for CSperMin
    cs_trace = go.Scatter(
        x=matchdf['gameCreation'],
        y=round(matchdf['CSperMin'], 2),
        mode='lines+markers',
        name='CSperMin',
        hovertemplate='%{y:.1f}'
    )

    # Creating traces for GoldperMin
    gold_trace = go.Scatter(
        x=matchdf['gameCreation'],
        y=round(matchdf['GoldperMin'], 2),
        mode='lines+markers',
        name='GoldperMin')

    fig.add_trace(vision_trace)
    fig.add_trace(cs_trace)
    fig.add_trace(gold_trace, secondary_y=True)

    fig.update_layout(title="Laning statistics", title_font_size=20,
                      height=400, font_color="#fafafa",
                      margin=dict(t=40, b=30),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      legend=dict(orientation="h", yanchor="top",
                                  xanchor="center", x=0.6, y=1.1))

    fig.update_yaxes(secondary_y=False,
                     range=[0, 10], showgrid=False, tickfont_color='#FAFAFA')
    fig.update_xaxes(title=None, showticklabels=False, showgrid=False, tickfont_color='#FAFAFA')
    fig.update_yaxes(secondary_y=True, showgrid=False, tickfont_color='#FAFAFA')
    fig.write_image("laning.png")