import discord, requests, json
from discord.ext import commands

class Dictionary():
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.server)
    async def define(self, ctx, word:str):

        if(word.lower() == "minecraft"):
            await self.bot.send_message(ctx.message.channel, word.lower() + " : The best game ever invented")
            return

        www = self.config["url"] + word.lower()
        r = requests.get(www, headers = {'app_id': self.config["app_id"], 'app_key': self.config["app_key"]})
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

def setup(bot, config):
    try:
        bot.add_cog(Dictionary(bot, config.oxford))
        print("[Dictionary Module Loaded]")
    except Exception as e:
        print(" >> Dictionary Module: {0}".format(e))