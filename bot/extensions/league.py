import hikari
import lightbulb
from ..utils.config import settings
from ..utils.embed import *
from ..utils.riot import *
from ..utils.opgg import *

plugin = lightbulb.Plugin("Riot", "📝 Player info")

GUILD = settings.GUILD
CHANNEL = settings.STDOUT_CHANNEL_ID
KEY = settings.RIOT

puuids = {
    'tuandao1311': '8UIhStkspIglog9paowA4mXzlckT-xySwWNIFac3o2ojumva9ffkFMda_jGpW_hhInKWpvUp5pPPrA',
    'cozybearrrrr': 'mh3B8Naz1MbJ6RE7dJTu3ZCLh7Rwo6CCJQiA-fVlLXUuQmkibMVMztpCLALJMMJQm4QOevN1-u0lnA',
    'tuanancom': 'DV0Aad31H16g3lItoojolWMPZQYOj0l90KzVSUV-qF3QlF92hOC_WLLssdR1MqPS-3UMEKp0Mn5woA',
    'nauqh': 'aTa5_43m0w8crNsi-i9nxGpSVU06WZBuK-h9bZEOK0g_lJox3XF4Dv4BzVwZieRj0QwlGnJ4SZbftg',
    'wavepin': 'idASdW5eSrO5Oih-ViK07RdeXE33JM1Mm3FwV7JiveTwbqfjl1vQUvToJ95c1B4EeQd8BAZgXkGSUw'
}

queues = {
    "Ranked Flex": 440,
    "Ranked Solo": 420,
    "ARAM": 450,
    "Normal Blind": 430,
    "Normal Draft": 400
}


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


@plugin.command()
@lightbulb.option('version', 'Patch notes version e.g. 14-3')
@lightbulb.command('patch', 'Latest patch notes', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def patch(ctx: lightbulb.Context):
    version = ctx.options.version.replace('.', '-')

    url = f"https://www.leagueoflegends.com/en-us/news/game-updates/patch-{version}-notes/"
    embed = patch_embed(version, url)
    await ctx.respond(embed)


@plugin.command()
@lightbulb.option('queue', 'Queue type', choices=['Ranked Flex',
                                                  'Ranked Solo',
                                                  'ARAM',
                                                  'Normal Blind',
                                                  'Normal Draft'], required=False)
@lightbulb.option('region', 'Region', default="VN2", choices=['VN2',
                                                              'OC1'], required=False)
@lightbulb.option('tag', 'Tagline')
@lightbulb.option('summoner', 'Summoner name')
@lightbulb.command('profile', 'Summoner profile with ranks, champions, last game, etc.', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def profile(ctx: lightbulb.Context) -> None:
    summoner, tag, region = ctx.options['summoner'], ctx.options['tag'], ctx.options['region']
    url = f"https://www.op.gg/summoners/{'vn' if region == 'VN2' else region}/{summoner.replace(' ', '%20')}-{tag}"
    puuid = get_puuid(KEY, summoner, tag)

    info = get_info(KEY, puuid, region)
    rank = get_rank(KEY, info, region)[0]
    champions = get_champions(summoner, tag)

    embed = profile_embed(
        info, rank, region, url,
        champions[:3], summoner, tag
    ).set_footer(
        text=f"Requested by {ctx.member.display_name}",
        icon=ctx.member.avatar_url
    )

    await ctx.respond(embed)


@plugin.command()
@lightbulb.option('champion', 'Champion name')
@lightbulb.command('build', 'Champion build', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def build(ctx: lightbulb.Context):
    champion = ctx.options['champion']

    try:
        header, url, runes = get_runes(champion)
        items = get_items(champion)
        embed = build_embed(
            champion, header, url,
            runes, items
        ).set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url)
        await ctx.respond(embed)
    except Exception:
        await ctx.respond(f"Cannot find champion name {champion}")
