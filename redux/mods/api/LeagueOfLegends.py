import discord
from discord.ext import commands
import requests, json, operator
import config

class LeagueOfLegends:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
    def fetch(self, url):
        r = requests.get(url)
        return json.loads(json.dumps(r.json()))
    def error(self, dict):
        try:
            return dict['status']['status_code']
        except KeyError:
            return None
    def scrubMatches(self, matches):
        results = dict()
        lanes = dict()
        for match in matches:
            if match['lane'] in lanes.keys():
                lanes[match['lane']] += 1
            else:
                lanes[match['lane']] = 1
        results['lane'] = (max(lanes.items(), key=operator.itemgetter(1))[0]).lower()
        return results

    def analyze(self, summoner:str):
        results = dict()
        results['error'] = 'none'

        jsonDict = self.fetch(self.config['summoner_url'] + summoner + "?api_key=" + self.config['key'])
        if self.error(jsonDict) != None:
            results['error'] = jsonDict['status']['status_code']
            return results
        results['id'] = jsonDict['accountId']
        results['level'] = jsonDict['summonerLevel']
        results['profile_image_url'] = self.config['profile_image_url'] + str(jsonDict['profileIconId']) + ".png"

        jsonDict = self.fetch(self.config['match_url'] + str(results['id']) + "?api_key=" + self.config['key'] + "&beginIndex=0&endIndex=10")
        if self.error(jsonDict) != None:
            results['error'] = jsonDict['status']['status_code']
            return results
        results['lane'] = self.scrubMatches(jsonDict['matches'])['lane']

        return results

    @commands.command(pass_context = True)
    async def lol(self, ctx):
        args = (ctx.message.content).split()[1:]
        summoner = (" ").join(args)

        results = self.analyze(summoner)
        if results['lane'] != "jungle":
            results['lane'] += " lane"
        else:
            results['lane'] = " the Jungle"


        embed = discord.Embed(title="League of Legend Stats", description="~Courtesy of Redux", color=0x00ff00)
        embed.add_field(name="Summoner", value=summoner + "(" + str(results['id']) + ")", inline=True)
        embed.add_field(name="Level", value=str(results['level']), inline=True)
        embed.add_field(name="Usually plays in ", value=results['lane'], inline=False)
        #embed.set_image(url=results['profile_image_url'])
        embed.set_thumbnail(url=results['profile_image_url'])
        await self.bot.send_message(ctx.message.channel, embed=embed)


def setup(bot):
    try:
        bot.add_cog(LeagueOfLegends(bot, config.league_of_legends))
        print("[LoL Module Loaded]")
    except Exception as e:
        print(" >> LoL Module: {0}".format(e))