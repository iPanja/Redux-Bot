import discord, requests, json
from discord.ext import commands
import config

class Dictionary():
    def __init__(self, bot, config):
        self.bot = bot
        self.config = dict()
        self.config["oxford"] = config[0]
        self.config["urban"] = config[1]

    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.server)
    async def define(self, ctx, word:str):

        if(word.lower() == "minecraft"):
            await self.bot.send_message(ctx.message.channel, word.lower() + " : The best game ever invented")
            return

        www = self.config["oxford"]["url"] + self.config["oxford"]["language"] + "/" + word.lower()
        r = requests.get(www, headers = {'app_id': self.config["oxford"]["app_id"], 'app_key': self.config["oxford"]["app_key"]})
        if (r.status_code == 404):
            await self.bot.send_message(ctx.message.channel, word.lower() + " is not a word!")
            return
        elif(r.status_code == 500):
            await self.bot.send_message(ctx.message.channel, "The Dictionary API is currently down.")
            return

        jsonDict = json.loads(json.dumps(r.json()))
        definition = jsonDict["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
        embed = discord.Embed(title="Oxford Dictionary", description="~Courtesy of Redux", color=0x00ff00)
        embed.add_field(name="Definition ", value=definition)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.server)
    async def urban(self, ctx, word:str):
        args = (ctx.message.content).split()[1:]
        word = (" ").join(args)
        query = ("%20").join(args)
        www = self.config["urban"]["url"] + query
        r = requests.get(www)
        jsonDict = json.loads(json.dumps(r.json()))
        if(jsonDict["result_type"] == "no_results"):
            await self.bot.send_message(ctx.message.channel, word.lower() + " : is not a word")
        else:
            embed = discord.Embed(title="Urban Dictionary", description="~Courtesy of Redux", color=0x00ff00)

            definition = jsonDict["list"][0]["definition"]
            if len(definition) > 200:
                definition = definition[:200]

            embed.add_field(name="Definition", value=definition)
            embed.add_field(name="More Info", value=self.config["urban"]["page"] + query)
            await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    try:
        bot.add_cog(Dictionary(bot, [config.oxford, config.urban]))
        print("[Dictionary Module Loaded]")
    except Exception as e:
        print(" >> Dictionary Module: {0}".format(e))