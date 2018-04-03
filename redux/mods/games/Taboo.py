import discord, asyncio, threading, json
from discord.ext import commands
from random import *
import config

class Taboo:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.loaded = False #Why load the cards at the beginning when the bot is restarted often and people might not play this game?
    def load(self):
        with open(self.config["card_loc"], 'r') as file:
            self.cards = json.load(file)
            self.keys = list(self.cards.keys())
    @commands.group(pass_context=True)
    async def taboo(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,
                                        "Please use a subcommand, view the link below for more information.\nhttps://github.com/PanjaCo/Redux-Bot/")
        else:
            await self.bot.delete_message(ctx.message)
    @taboo.command(pass_context = True)
    async def new(self, ctx):
        if not self.loaded:
            self.load()
            self.loaded = True
        card = self.keys[randint(0, len(self.keys)-1)]
        blacklist = self.cards[card]

        blacklistString = ""
        for word in blacklist:
            blacklistString += word.title() + "\n"

        embed = discord.Embed(title="Taboo", description="~Couresty of Redux", color=0x00ff00)
        embed.add_field(name="Word", value=card.title(), inline=False)
        embed.add_field(name="Words you can NOT say", value=blacklistString, inline=False)

        await self.bot.send_message(ctx.message.author, embed=embed)

def setup(bot):
    try:
        bot.add_cog(Taboo(bot, config.taboo))
        print("[Taboo Module Loaded]")
    except Exception as e:
        print(" >> Taboo Module: {0}".format(e))