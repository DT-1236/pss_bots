from discord.ext import commands
# pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py

from pss_bot.bot import PSSBot
from configs import pss_bot_config

bot = commands.Bot(command_prefix='?', case_insensitive=True)
pss = PSSBot()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(aliases=['renew, reboot'])
async def refresh(ctx):
    global pss
    pss = PSSBot()
    await ctx.send("Crew and Equipment Values have been refreshed")
    return


@bot.command(aliases=['stat'])
async def stats(ctx, *, raw_input: str):
    """: 1 crew = > Full stats including equipment interactions for requested crew ;
     crew, crew => Stat comparison between the two crew members"""

    user_input = pss.prepare_user_input(raw_input)
    if not user_input:
        await ctx.send(stats.__doc__)
        return

    matched_xmls, messages = pss.get_crew_xml_from_user_input(user_input)
    for message in messages:
        await ctx.send(message)
    if len(matched_xmls) == 1:
        await ctx.send(pss.base_stat_output(*matched_xmls))
        await ctx.send(pss.max_stat_output(*matched_xmls))
        return
    else:
        await ctx.send(pss.base_stat_comparison(*matched_xmls))
        await ctx.send(pss.max_stat_comparison(*matched_xmls))
        return


@bot.command(aliases=['train'])
async def training(ctx, value: float):
    """Changes the reference training value"""
    pss.training = value
    await ctx.send("Reference training value set to {}%".format(pss.training))
    return


@bot.command()
async def test(ctx, *, raw_input: str):
    print(raw_input)
    await ctx.send(raw_input)

bot.run(pss_bot_config.token)
