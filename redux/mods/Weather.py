import discord, requests, json
from discord.ext import commands
import config
from pprint import pprint

class Weather:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def weather(self, ctx):
        args = (ctx.message.content).split()[1:]
        query = " ".join(args)

        isInt = False
        try:
            int(query)
            isInt = True
        except ValueError:
            isInt = False

        if isInt:
            #ZIPCODE
            www = self.config['url'] + "zip=" + query
        else:
            #City
            www = self.config['url'] + "q=" + query
        www += "&appid=" + self.config["key"]

        r = requests.get(www)
        jsonDict = json.loads(json.dumps(r.json()))
        if(jsonDict['cod'] == 401):
            await self.bot.send_message(ctx.message.channel, "A Dev Caused Problem Has Occurred, ERROR: API_KEY")
            return
        elif(jsonDict['cod'] == 400):
            await self.bot.send_message(ctx.message.channel, "Invalid Location, please contact a developer")
            return
        elif(jsonDict['cod'] == 404):
            await self.bot.send_message(ctx.message.channel, "Location not found")
            return

        embed = discord.Embed(title="Weather", description="~Open Weather Map", color=0x00ff00)
        embed.add_field(name=jsonDict['name'], value=jsonDict['sys']['country'])
        embed.add_field(name=jsonDict['weather'][0]['main'], value=jsonDict['weather'][0]['description'])
        embed.add_field(name="Temperature", value=jsonDict['main']['temp'])
        embed.add_field(name="Pressure", value=jsonDict['main']['pressure'])
        embed.add_field(name="Humidity", value=jsonDict['main']['humidity'])
        embed.add_field(name="Wind Speed", value=jsonDict['wind']['speed'])

        await self.bot.send_message(ctx.message.channel, embed=embed)
def setup(bot):
    try:
        bot.add_cog(Weather(bot, config.open_weather_map))
        print("[Weather Module Loaded]")
    except Exception as e:
        print(" >> Weather Module: {0}".format(e))