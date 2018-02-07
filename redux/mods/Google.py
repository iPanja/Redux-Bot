import discord
from discord.ext import commands
import requests, json
from pprint import pprint

""" Google AIP Keys """
urlshorten_key = "AIzaSyD30QQMxQWKQbDiIwEI1Z-vo7rGQnDmtMQ"

class Google:
    def __init__(self, bot, keys):
        self.bot = bot
        self.urlshorten_key = keys[0]
    @commands.command(pass_context=True)
    async def shorten(self, ctx, url:str):
        gUrl = "https://www.googleapis.com/urlshortener/v1/url?key=" + self.urlshorten_key
        payload = {"longUrl" : url}
        headers = {"content-type" : "application/json"}
        r = requests.post(gUrl, data=json.dumps(payload), headers=headers)
        jsonDict = json.loads(json.dumps(r.json()))
        newUrl = jsonDict["id"]
        await self.bot.send_message(ctx.message.channel, newUrl)
    @commands.command(pass_context=True)
    async def expand(self, ctx, url:str):
        gUrl = "https://www.googleapis.com/urlshortener/v1/url?key=" + self.urlshorten_key + "&&shortUrl=" + url
        headers = {"content-type" : "application/json"}
        r = requests.get(gUrl, headers=headers)
        jsonDict = json.loads(json.dumps(r.json()))
        oldUrl = jsonDict["longUrl"]
        await self.bot.send_message(ctx.message.channel, oldUrl)

def setup(bot):
    try:
        bot.add_cog(Google(bot, [urlshorten_key]))
        print("[Google Module Loaded]")
    except Exception as e:
        print(" >> Google Module: {0}".format(e))