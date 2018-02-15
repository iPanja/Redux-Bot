import discord
from discord.ext import commands
from py_expression_eval import Parser

class Math:
    def __init__(self, bot):
        self.bot = bot
        self.parser = Parser()
        self.eq = ""
        self.vars = dict()
    @commands.command(pass_context = True)
    async def solve(self, ctx):
        eval = self.parser.parse(self.eq).evaluate(self.vars)
        await self.bot.send_message(ctx.message.channel, "Answer: " + str(eval))
        #Reset
        self.eq = ""
        self.vars = dict()
    @commands.command(pass_context = True)
    async def equation(self, ctx):
        args = (ctx.message.content).split()[1:]
        self.eq = (" ").join(args)
        if(self.eq == "9 + 10"):
            await self.bot.send_message(ctx.message.channel, "twenty-juan")
    @commands.command(pass_context = True)
    async def variable(self, ctx, var:str, val:int):
        self.vars[var] = val

def setup(bot):
    try:
        bot.add_cog(Math(bot))
        print("[Math Module Loaded]")
    except Exception as e:
        print(" >> Math Module: {0}".format(e))