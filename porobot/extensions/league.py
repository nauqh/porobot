from datetime import datetime
from ..config import settings
from ..utils import *
from ..riot import *
from ..embed import *
from requests import get

import hikari
import lightbulb

"""
League of Legends statistics
"""

plugin = lightbulb.Plugin("Riot", "📝 Player info")

GUILD_ID = settings.GUILD
CHANNEL = settings.STDOUT_CHANNEL_ID
VOICE = settings.VOICE_CHANNEL_ID

members = {"Cozy Bearrrrr": 'Cozy Bearrrrr',
           "ancomsuon": 'UnbeatableVN',
           "urbestbae": '3 Giờ Rửa Chim',
           "iu vk thungan": 'Lushen2711',
           "Obi-Wan": 'Sứ Giả Lọk Khe'}


@plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    author = event.state.member
    api_key = settings.RIOT
    region = 'vn2'
    mass_region = "sea"
    no_games = 5
    queue_id = 450

    if event.state.channel_id != None:
        return
    try:
        summoner_name = members[author.display_name]
    except Exception:
        return

    # TODO: Get puuid and list of match ids
    puuid = get_puuid(summoner_name, region, api_key)
    match_ids = get_match_ids(puuid, mass_region, no_games, queue_id, api_key)
    msg = await plugin.bot.rest.create_message(settings.STDOUT_CHANNEL_ID, "...")

    # TODO: Gather data
    matches = []
    player = []

    count = 0
    total = len(match_ids)
    for match_id in match_ids:
        match_data = get_match_data(match_id, mass_region, api_key)
        player_data = find_player_data(match_data, puuid)
        matches.append(match_data['info'])
        player.append(player_data)

        await msg.edit(progress_bar(count/total))
        count += 1
    await msg.edit("📦")

    # Dataframe of all players of 5 games (5 x 10 records)
    df = pd.json_normalize(matches)
    # Dataframe of player of 5 games
    player_df = pd.json_normalize(player)

    stats = transform(df, player_df)

    # TODO: Aggregate and display
    embed = (
        hikari.Embed(
            title=f"{author.username} - Most recent games",
            description=f"**Champion pool**: {', '.join(stats['champions'])}",
            colour="#9bf6ff",
            timestamp=datetime.now().astimezone(),
            url=f"https://www.op.gg/summoners/vn/{summoner_name.replace(' ', '%20')}"
        ).set_thumbnail(author.avatar_url)
        .add_field(
            '🎯 **Games**',
            f"{stats['wins'] + stats['loses']}G {stats['wins']}W {stats['loses']}L",
            inline=True
        )
        .add_field(
            '🏆 **Winrates**',
            f"{round((stats['wins']/5), 2)*100} %",
            inline=True
        )
        .add_field(
            '**⚔️ KDA**',
            f"{stats['kills']}/{stats['deaths']}/{stats['assists']}",
            inline=True
        )
        .add_field(
            '🥊 **Damage**',
            stats['dmg'],
            inline=True
        ).add_field(
            '**Pentakills**',
            stats['penta'],
            inline=True
        )
        .add_field(
            '🤝 **Participation**',
            "68 %",
            inline=True
        )
        .add_field(
            f'🏆 **Achievements** - `{stats["badge"]}`',
            f"""
            **Time spent alive ❣️**: {round(stats['timealive']/60)}m {round(stats['timealive']%60)}s
            **Time in graves 🪦**: {round(stats['timedead']/60)}m {round(stats['timedead']%60)}s
            **CS per minute 🧠**: {stats['cspermin']}
            """,
            inline=True
        )
        .set_footer(
            text=f"Requested by {author.username}",
            icon=author.avatar_url
        ))

    await msg.edit(embed)
    if not stats['penta'] > 0:
        await plugin.bot.rest.create_message(settings.STDOUT_CHANNEL_ID, f"{author.mention} 🤡")
    else:
        await plugin.bot.rest.create_message(settings.STDOUT_CHANNEL_ID, f"{author.mention} Congratulations 🏆")


@plugin.command()
@lightbulb.option('version', 'Patch notes version')
@lightbulb.command('patch', 'Latest patch notes', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def patch(ctx: lightbulb.Context):
    version = ctx.options.version.replace('.', '-')

    url = f"https://www.leagueoflegends.com/en-us/news/game-updates/patch-{version}-notes/"
    embed = patch_emb(version, url)
    await ctx.respond(embed)


@plugin.command()
@lightbulb.command('rotation', 'Free week rotation.', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def play(ctx: lightbulb.Context, api_key="RGAPI-a384a673-d288-42ec-a860-55a1602dba94") -> None:
    rotation = get(
        f"https://vn2.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api_key}").json()

    patch = get(
        "https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    champions = requests.get(
        f"http://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json").json()['data']
    champ_ids = rotation['freeChampionIds']

    names = []
    for name in champions:
        if int(champions[name]['key']) in champ_ids:
            names.append(name)

    embed = rotation_emb(names)
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)
