from datetime import datetime
from ..config import settings
from ..utils import *
from ..riot import *
from ..data.db import *

import hikari
import lightbulb

"""
League of Legends statistics
"""

plugin = lightbulb.Plugin("Riot", "📝 Player info")

GUILD_ID = settings.GUILD
CHANNEL = settings.STDOUT_CHANNEL_ID
VOICE = settings.VOICE_CHANNEL_ID
db = init_database()
members = {"Cozy Bearrrrr": 'Cozy Bearrrrr',
           "ancomsuon": 'UnbeatableVN',
           "urbestbae": '3 Giờ Rửa Chim',
           "iu vk thungan": 'Lushen2711',
           "Obi-Wan": 'Sứ Giả Lọk Khe',
           "Wavepin": 'Wavepin'}


@plugin.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    author = event.state.member

    if event.state.channel_id != None:
        return
    try:
        summoner_name = members[author.display_name]
    except Exception:
        return

    msg = await plugin.bot.rest.create_message(settings.STDOUT_CHANNEL_ID, "...")
    stats = update_database(db, summoner_name)

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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)
