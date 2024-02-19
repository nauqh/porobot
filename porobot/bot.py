"""Porobot 

This module init bot app and run on hikari. The module 
contains some listeners for general events such as `starting`,
`started` and `stopping`

"""

import porobot
import hikari
import lightbulb
import logging
from .config import settings


log = logging.getLogger(__name__)

bot = lightbulb.BotApp(
    settings.TOKEN,
    intents=hikari.Intents.ALL,
    default_enabled_guilds=settings.GUILD,
    help_slash_command=True,
    banner=None,
)


# Extension
bot.load_extensions_from("./porobot/extensions", must_exist=True)


def run() -> None:
    bot.run(
        activity=hikari.Activity(
            name=f"v{porobot.__version__}",
            type=hikari.ActivityType.LISTENING,
            state="💡porodocs | /help")
    )
