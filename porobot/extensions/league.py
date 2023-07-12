from datetime import datetime
from ..config import settings
from ..utils import *

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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)
