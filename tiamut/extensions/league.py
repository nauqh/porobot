from datetime import datetime
from ..config import settings
from ..utils import *
from ..test import *

import hikari
import lightbulb

"""
Handle member information
"""

plugin = lightbulb.Plugin("League of Legends", "🎮 Champions info")

GUILD_ID = settings.GUILD
CHANNEL = settings.STDOUT_CHANNEL_ID
VOICE = settings.VOICE_CHANNEL_ID

members = {"Cozy Bearrrrr": 'Cozy Bearrrrr',
           "ancomsuon": 'UnbeatableVN',
           "urbestbae": '3 Giờ Rửa Chim',
           "iu vk thungan": 'Lushen2711',
           "Obi-Wan": 'Sứ Giả Lọk Khe'}


def progress_bar(percent: float) -> str:
    progress = ''
    for i in range(12):
        if i == (int)(percent*12):
            progress += '🔘'
        else:
            progress += '▬'
    return progress


@plugin.command
@lightbulb.option(
    "champion", "The champion to get information about.", required=True
)
@lightbulb.command(
    "get", "Get info about the champion.", auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def get(ctx: lightbulb.Context):
    champion = ctx.options.champion

    # TODO: VALIDATE
    error = runes(champion)
    if error == None:
        await ctx.respond(f"No champion name `{champion}`, try again")
    else:
        # TODO: RUNES
        primary = []
        rows = runes(champion)['primary']
        for row in rows:
            primary.append(get_main_rune(row))

        secondary = []
        rows = runes(champion)['secondary']
        for row in rows:
            if get_main_rune(row) == None:
                secondary.append("_")
            else:
                secondary.append(get_main_rune(row))

        # TODO: ITEMS
        items = build(champion, 3)

        embed = (
            hikari.Embed(
                title=f"**{champion.capitalize()}** Build",
                description=f"**Branch**: `{primary[1]}`",
                colour=0x9bf6ff,
                timestamp=datetime.now().astimezone(),
                url=f"https://www.op.gg/modes/aram/{champion}/build?region=kr"
            )
            .set_thumbnail(f"http://ddragon.leagueoflegends.com/cdn/13.13.1/img/champion/{champion.capitalize()}.png")
            .add_field(
                primary[2],
                secondary[1],
                inline=True
            )
            .add_field(
                primary[3],
                secondary[2],
                inline=True
            )
            .add_field(
                primary[4],
                secondary[3],
                inline=True
            )
            .add_field(
                "**Items**",
                ', '.join(items[0]),
                inline=False
            )
            .add_field(
                "**Alternatives**",
                ', '.join(items[1]),
                inline=True
            )
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
            )
        )

        await ctx.respond(embed)


@plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    author = event.state.member

    if event.state.channel_id != None:
        return

    api_key = settings.RIOT

    try:
        summoner_name = members[author.display_name]
    except Exception:
        return

    region = 'vn2'
    mass_region = "sea"
    no_games = 5
    queue_id = 450

    puuid = get_puuid(summoner_name, region, api_key)
    match_ids = get_match_ids(puuid, mass_region, no_games, queue_id, api_key)
    msg = await plugin.bot.rest.create_message(settings.STDOUT_CHANNEL_ID, "...")

    data = {
        'champion': [],
        'kills': [],
        'deaths': [],
        'assists': [],
        'win': [],
        'dmg': [],
        'quadkill': [],
        'pentakill': [],
        'teamkills': []
    }

    count = 0
    total = len(match_ids)
    for match_id in match_ids:
        match_data = get_match_data(match_id, mass_region, api_key)
        player_data = find_player_data(match_data, puuid)

        # assign the variables we're interested in
        champion = player_data['championName']
        k = player_data['kills']
        d = player_data['deaths']
        a = player_data['assists']
        win = player_data['win']
        dmg = player_data['totalDamageDealtToChampions']
        quad = player_data['quadraKills']
        penta = player_data['pentaKills']
        teamid = player_data['teamId']

        # add them to our dataset
        data['champion'].append(champion)
        data['kills'].append(k)
        data['deaths'].append(d)
        data['assists'].append(a)
        data['win'].append(win)
        data['dmg'].append(dmg)
        data['quadkill'].append(quad)
        data['pentakill'].append(penta)
        data['teamkills'].append(get_team_kills(match_data, teamid))

        await msg.edit(progress_bar(count/total))
        count += 1
    await msg.edit("📦")

    df = pd.DataFrame(data)
    wins = df['win'].value_counts().values[0]
    loses = df['win'].value_counts().values[1]
    penta = df['pentakill'].sum() + '👑' if df['pentakill'].sum() > 0 else '🤡'
    df['participation'] = (df['kills'] + df['assists']) / df['teamkills'] * 100

    embed = (
        hikari.Embed(
            title=f"{author.username} - Most recent games",
            description=f"**Champion pool**: {', '.join(df['champion'].unique().tolist())}",
            colour=author.accent_colour,
            timestamp=datetime.now().astimezone(),
            url=f"https://www.op.gg/summoners/vn/{summoner_name.replace(' ', '%20')}"
        )
        .set_thumbnail(author.avatar_url)
        .add_field(
            '🎯 **Games**',
            f"{len(df)}G {wins}W {loses}L",
            inline=True
        )
        .add_field(
            '🏆 **Winrates**',
            f"{(wins/len(df))*100} %",
            inline=True
        )
        .add_field(
            '**⚔️ KDA**',
            f"{df['kills'].mean()}/{df['deaths'].mean()}/{df['assists'].mean()}",
            inline=True
        )
        .add_field(
            '🥊 **Damage**',
            df['dmg'].mean(),
            inline=True
        ).add_field(
            '**Pentakills**',
            penta,
            inline=True
        )
        .add_field(
            '🤝 **Participation**',
            f"{df['teamkills'].mean()} %",
            inline=True
        )
        .add_field(
            '🎖️ **Achievements**',
            f"**The unded**: nienvinvienv \n `The inovator`: ievbiebvibeibvebi",
            inline=True
        )
        .set_footer(
            text=f"Requested by {author.username}",
            icon=author.avatar_url
        )
    )

    await msg.edit(embed)

    if not df['pentakill'].sum() > 0:
        await plugin.bot.rest.create_message(settings.STDOUT_CHANNEL_ID, f"{author.mention} 🤡")
    else:
        await plugin.bot.rest.create_message(settings.STDOUT_CHANNEL_ID, f"{author.mention} Congratulations 🏆")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)
