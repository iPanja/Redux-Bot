import discord
from discord.ext import commands

class Appearance():
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context = True)
    async def updateBot(self, ctx, gameName:str):
        guildsCount = len(self.bot.servers)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds=guildsCount, members=memberCount)
        await self.bot.change_presence(game=discord.Game(name=gameName))

def setup(bot):
    try:
        bot.add_cog(Appearance(bot))
        print("[Appearance Module Loaded]")
    except Exception as e:
        print(" >> Appearance Module: {0}".format(e))