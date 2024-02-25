import bot
import hikari
import lightbulb
from .utils.config import settings


app = lightbulb.BotApp(
    settings.TOKEN,
    intents=hikari.Intents.ALL,
    default_enabled_guilds=settings.GUILD,
    help_slash_command=True,
    banner=None
)

# Extensions
app.load_extensions_from("./bot/extensions", must_exist=True)


def run() -> None:
    app.run(
        activity=hikari.Activity(
            name=f"v{bot.__version__}",
            type=hikari.ActivityType.LISTENING,
            state="💡porodocs | /help")
    )
