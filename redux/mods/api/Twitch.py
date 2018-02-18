""" DOES NOT WORK --- Will be fixed in a future update"""


import discord, requests, json
from discord.ext import commands
import config
from pprint import pprint

class Twitch:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.headers = {'Authorization' : 'Client-ID ' + config['client_id']}
    @commands.command(pass_context = True)
    async def tGameStreamers(self, ctx):
        query = "".join((ctx.message.content).split()[1:])
        game = self.getGame(query)

        www = self.config['url'] + 'streams?first=3&game_id=' + game.id
        r = requests.get(www, headers=self.headers)
        jsonDict = json.loads(json.dumps(r.json()))
        pprint(jsonDict)
        streamers = list()
        for s in jsonDict['data']:
            streamer = Streamer(s['id'], s['user_id'], s['type'], s['title'], s['viewer_count'])
            streamer = self.getName(streamer)

        embed = discord.Embed(title=game.name, description="Top streamers")
        for s in streamers:
            embed.add_field(name=s.name, value=s.type)
            embed.add_field(name="Title", value=s.title)
            embed.add_field(name="Viewers", value=s.viewer_count)
            embed.add_field(name="------------------------------")
        await self.bot.send_message(ctx.message.channel, embed=embed)


    def getGame(self, gameName):
        www = self.config['url'] + 'games/?name=' + gameName
        r = requests.get(www, headers=self.headers)
        jsonDict = json.loads(json.dumps(r.json()))
        pprint(jsonDict)
        game = Game(jsonDict[0]['id'], jsonDict[0]['name'], jsonDict[0]['box_art_url'])
        return game
    def getName(self, streamer):
        www = self.config['url'] + 'users/?id=' + streamer.user_id
        r = requests.get(www, headers=self.headers)
        jsonDict = json.loads(json.dumps(r.json()))
        pprint(jsonDict)
        streamer.name = jsonDict[0]['display_name']
        return streamer

class Game:
    def __init__(self, id, name, box_art_url):
        self.id = id
        self.name = name
        self.box_art_url = box_art_url
class Streamer:
    def __init__(self, id, user_id, type, title, viewer_count, name=None):
        self.id = id
        self.user_id = user_id
        self.type = type
        self.title = title
        self.viewer_count = viewer_count
        self.name = name
def setup(bot):
    try:
        bot.add_cog(Twitch(bot, config.twitch))
        print("[Twitch Module Loaded]")
    except Exception as e:
        print(" >> Twitch Module: {0}".format(e))