import discord
from discord.ext import commands
import requests, json
import config

class Google:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    @commands.command(pass_context=True)
    async def shorten(self, ctx, url:str):
        gUrl = "https://www.googleapis.com/urlshortener/v1/url?key=" + self.config["urlshorten_key"]
        payload = {"longUrl" : url}
        headers = {"content-type" : "application/json"}
        r = requests.post(gUrl, data=json.dumps(payload), headers=headers)
        jsonDict = json.loads(json.dumps(r.json()))
        newUrl = jsonDict["id"]
        await self.bot.send_message(ctx.message.channel, newUrl)
    @commands.command(pass_context=True)
    async def expand(self, ctx, url:str):
        gUrl = "https://www.googleapis.com/urlshortener/v1/url?key=" + self.config["urlshorten_key"] + "&&shortUrl=" + url
        headers = {"content-type" : "application/json"}
        r = requests.get(gUrl, headers=headers)
        jsonDict = json.loads(json.dumps(r.json()))
        oldUrl = jsonDict["longUrl"]
        await self.bot.send_message(ctx.message.channel, oldUrl)

def setup(bot):
    try:
        bot.add_cog(Google(bot, config.google))
        print("[Google Module Loaded]")
    except Exception as e:
        print(" >> Google Module: {0}".format(e))