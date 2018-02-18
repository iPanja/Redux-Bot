import discord
from discord.ext import commands
from alpha_vantage.timeseries import TimeSeries
import config

class Market:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    @commands.command(pass_context = True)
    async def stock(self, ctx, ticker:str):
        ts = TimeSeries(key=self.config["key"], output_format="json")
        data, meta_data = ts.get_daily(symbol=ticker, outputsize="compact")

        current = data[list(data.keys())[0]]
        for i,_ in enumerate(current.keys()):
            entry = current[list(current.keys())[i]]
            value = round(float(entry), 2)
            current[list(current.keys())[i]] = str(value)
        #EMBED
        embed = discord.Embed(title=ticker.upper(), description="Daily Stock Info", color=0x00ff00)
        embed.add_field(name="Opened:", value="$" + current['1. open'], inline=True)
        embed.add_field(name="Closed:", value="$" + current['4. close'], inline=True)
        embed.add_field(name="Low:", value="$" + current['3. low'], inline=True)
        embed.add_field(name="High", value="$" + current['2. high'], inline=True)
        await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
    try:
        bot.add_cog(Market(bot, config.alpha_vantage))
        print("[Market Module Loaded]")
    except Exception as e:
        print(" >> Market Module: {0}".format(e))