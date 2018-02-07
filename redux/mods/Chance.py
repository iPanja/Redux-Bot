import discord
from discord.ext import commands
import random

class Chance:
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context=True)
    async def randcard(self, ctx):
        suits = ["H", "D", "C", "S"]
        cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        suit = suits[random.randint(0, 3)]
        card = cards[random.randint(0, 12)]
        await self.bot.send_message(ctx.message.channel, suit + str(card))
    @commands.command(pass_context=True)
    async def randint(self, ctx, min:int, max:int):
        await self.bot.send_message(ctx.message.channel, str(random.randint(min, max)))
    @commands.command(pass_context=True)
    async def rolldie(self, ctx, sides:int = 6):
        await self.bot.send_message(ctx.message.channel, str(random.randint(1, sides)))
    @commands.command(pass_context=True)
    async def rolldice(self, ctx, sides:int = 6):
        results = []
        for i in range (0, 2):
            results.append(random.randint(1, sides))
        await self.bot.send_message(ctx.message.channel, str(results[0]) + ", " + str(results[1]))
    @commands.command(pass_context=True)
    async def flipcoin(self, ctx):
        options = ["Heads", "Tails"]
        await self.bot.send_message(ctx.message.channel, "" + options[random.randint(0, 1)])
    #
    #Raffle
    #
    @commands.command(pass_context=True)
    async def rcreate(self, ctx, max=None):
        self.rPlayers = list()
        self.max = max
        await self.bot.send_message(ctx.message.channel, "The raffle has begun")
    @commands.command(pass_context=True)
    async def renter(self, ctx):
        if self.max != None and (len(self.rPlayers)+1 > self.max):
            await self.bot.send_message(ctx.message.channel, "The raffle has reached max capacity, sorry!")
            return
        self.rPlayers.append(ctx.message.author)
        await self.bot.send_message(ctx.message.channel, "You have entered the raffle!")
    @commands.command(pass_context=True)
    async def rend(self, ctx):
        await self.bot.send_message(ctx.message.channel, "The raffle has ended. The winner is: " + self.rPlayers[random.randint(0, len(self.rPlayers)-1)].display_name)

def setup(bot):
    try:
        bot.add_cog(Chance(bot))
        print("[Chance Module Loaded]")
    except Exception as e:
        print(" >> Chance Module: {0}".format(e))