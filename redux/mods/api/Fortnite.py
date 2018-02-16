import discord, requests, json
from discord.ext import commands
import difflib
import config

class Fortnite:
    def __init__(self, bot, config):
        self.bot = bot
        self.data = dict()
        self.keys = []
        self.config = config
        with open(config["weapon_data_loc"], 'r') as f:
            self.data = json.load(f)
            self.keys = list(self.data.keys())
    def send_request(self, platform, username):
        r = requests.get(self.config["url"] + platform + '/' + username)
        response = r.text
        try:
            player_data = json.loads(self.find_between(response, 'var playerData = ', ';</script>'))
            account_info = json.loads(self.find_between(response, 'var accountInfo = ', ';</script>'))
            lifetime_stats = json.loads(self.find_between(response, 'var LifeTimeStats = ', ';</script>'))
        except Exception:
            return ''

        return [player_data, account_info, lifetime_stats]
    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def flookup(self, ctx, platform:str, player:str):
        r = self.send_request(platform.lower(), player.lower())

        try:
            solo = r[0]['p2']
        except IndexError:
            await self.bot.send_message(ctx.message.channel, "Player not found")

        embed = discord.Embed(title="Fortnite Stats", description="~TRN Network", color=0x00ff00)
        embed.add_field(name="K/D", value=solo[9]['displayValue'], inline=False)
        embed.add_field(name="Score", value=solo[1]['displayValue'], inline=True)
        embed.add_field(name="Top 25", value=solo[8]['displayValue'], inline=True)
        embed.add_field(name="Time Played", value=solo[12]['displayValue'], inline=True)

        await self.bot.send_message(ctx.message.channel, embed=embed)
    @commands.command(pass_context = True)
    async def fstats(self, ctx):
        args = (ctx.message.content).split()[1:]
        query = (" ").join(args)
        matches = (difflib.get_close_matches(query, self.keys))

        if(len(matches) == 0):
            await self.bot.send_message(ctx.message.channel, "No weapon found")
        else:
            match = self.data[matches[0]]

            msg = matches[0] + ":\n"
            msg += "    Damage: " + match["damage"] + "\n"
            msg += "    DPS: " + match["dps"] + "\n"
            msg += "    Mag Size: " + match["mag_size"] + "\n"
            msg += "    Rarity: " + match["rarity"] + "\n"
            msg += "    Type: " + match["type"] + "\n"

            embed = discord.Embed(title="Fortnite Weapon Stats", description="~Courtesy of Redux", color=0x00ff00)
            embed.add_field(name=matches[0], value=match['type'], inline=False)
            embed.add_field(name="Damage", value=match['damage'])
            embed.add_field(name="DPS", value=match['dps'])
            embed.add_field(name="Mag Size", value=match['mag_size'])
            embed.add_field(name="Rarity", value=match['rarity'])

            await self.bot.send_message(ctx.message.channel, embed=embed)
def setup(bot):
    try:
        bot.add_cog(Fortnite(bot, config.fortnite))
        print("[Fortnite Module Loaded]")
    except Exception as e:
        print(" >> Fortnite Module: {0}".format(e))