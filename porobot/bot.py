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
bot.load_extensions_from("./tiamut/extensions", must_exist=True)


@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    ...


@bot.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    await bot.rest.create_message(
        settings.STDOUT_CHANNEL_ID,
        f"📈 Poro is now online! (Version {porobot.__version__})",
    )


@bot.listen(hikari.StoppingEvent)
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.rest.create_message(
        settings.STDOUT_CHANNEL_ID,
        f"📉 Poro is shutting down. (Version {porobot.__version__})",
    )


def run() -> None:
    bot.run(
        activity=hikari.Activity(
            name=f"/help • Version {porobot.__version__}",
            type=hikari.ActivityType.WATCHING,
        )
    )
