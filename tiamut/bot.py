import tiamut
import hikari
import lightbulb
import miru
import logging
from .config import settings


class BasicView(miru.View):

    # Define a new TextSelect menu with two options
    @miru.text_select(
        placeholder="Select me!",
        options=[
            miru.SelectOption(label="Option 1"),
            miru.SelectOption(label="Option 2"),
        ],
    )
    async def basic_select(self, select: miru.TextSelect, ctx: miru.ViewContext) -> None:
        await ctx.respond(f"You've chosen {select.values[0]}!")

    # Define a new Button with the Style of success (Green)
    @miru.button(label="Click me!", style=hikari.ButtonStyle.SUCCESS)
    async def basic_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.respond("You clicked me!")

    # Define a new Button that when pressed will stop the view & invalidate all the buttons in this view
    @miru.button(label="Stop me!", style=hikari.ButtonStyle.DANGER)
    async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        self.stop()  # Called to stop the view


log = logging.getLogger(__name__)

bot = lightbulb.BotApp(
    settings.TOKEN,
    intents=hikari.Intents.ALL,
    default_enabled_guilds=settings.GUILD,
    help_slash_command=True,
    banner=None,
)

miru.install(bot)

# Extension
bot.load_extensions_from("./tiamut/extensions", must_exist=True)


@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    ...


@bot.listen(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    await bot.rest.create_message(
        settings.STDOUT_CHANNEL_ID,
        f"📈 Tiamut is now online! (Version {tiamut.__version__})",
    )


@bot.listen()
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    # Ignore bots or webhooks pinging us
    if not event.is_human:
        return

    me = bot.get_me()

    # If the bot is mentioned
    if me.id in event.message.user_mentions_ids:
        view = BasicView(timeout=60)  # Create a new view
        message = await event.message.respond("Hello miru!", components=view)
        await view.start(message)  # Start listening for interactions
        await view.wait()  # Optionally, wait until the view times out or gets stopped
        await event.message.respond("Goodbye!")


@bot.listen(hikari.StoppingEvent)
async def on_stopping(_: hikari.StoppingEvent) -> None:
    await bot.rest.create_message(
        settings.STDOUT_CHANNEL_ID,
        f"📉 Tiamut is shutting down. (Version {tiamut.__version__})",
    )


def run() -> None:
    bot.run(
        activity=hikari.Activity(
            name=f"/help • Version {tiamut.__version__}",
            type=hikari.ActivityType.WATCHING,
        )
    )
