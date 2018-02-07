import discord, requests, json
from discord.ext import commands

""" -- Config -- """
app_id = "e582bbc3"
app_key = "aa47642455e4b44dae35038c7b85c4ac"
language = "en"
url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/'

class Dictionary():
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.server)
    async def define(self, ctx, word:str):

        if(word.lower() == "minecraft"):
            await self.bot.send_message(ctx.message.channel, word.lower() + " : The best game ever invented")
            return

        www = url + word.lower()
        r = requests.get(www, headers = {'app_id': app_id, 'app_key': app_key})
        if (r.status_code == 404):
            await self.bot.send_message(ctx.message.channel, word.lower() + " is not a word!")
            return
        elif(r.status_code == 500):
            await self.bot.send_message(ctx.message.channel, "The Dictionary API is currently down.")
            return
        else:
            print(r.status_code)

        jsonDict = json.loads(json.dumps(r.json()))

        definition = jsonDict["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
        await self.bot.send_message(ctx.message.channel, word.lower() + " : " + definition)

def setup(bot):
    try:
        bot.add_cog(Dictionary(bot))
        print("[Dictionary Module Loaded]")
    except Exception as e:
        print(" >> Dictionary Module: {0}".format(e))