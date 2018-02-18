import discord
from discord.ext import commands
import config

#Discord API
discordToken = config.discord["key"]
bot = discord.Client()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='TSA 2018 Bot')

modules = [
    'mods.Moderation',
    'mods.Appearance',
    'mods.api.Dictionary',
    'mods.games.Blackjack',
    'mods.api.Fortnite',
    'mods.Math',
    'mods.Vote',
    'mods.Music',
    'mods.Chance',
    'mods.api.Google',
    'mods.api.Market',
    'mods.api.Weather',
    'mods.api.Reddit',
    'mods.games.Connect4'
]

for cog in modules:
    try:
        bot.load_extension(cog)
    except Exception as e:
        message = 'Failed to load module {0}\n{1} : {2}'.format(cog, type(e).__name__, e)
        bot.send_message("368100617543221260", message)
        print(message)

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
    """
    await bot.edit_profile(username="Redux")
    with open('F:\Fletcher\Pictures\logo.png', 'rb') as f:
        await bot.edit_profile(avatar=f.read())
    """
@bot.event
async def on_message(message):
    await bot.get_cog("Moderation").scrub(message)
    await bot.process_commands(message)
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after);
        return;
    if isinstance(error, commands.CommandNotFound):
        return
    raise error;

bot.run(discordToken)
