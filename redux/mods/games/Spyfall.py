import discord, asyncio, threading
from discord.ext import commands
from random import *
import config

class Spyfall:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.reset()
    def reset(self):
        self.state = 0 #0 = GameOver    1 = Game Started    2 = Done. Spy Lost      3 = Done. Spy Won
        self.voted = list()
        self.players = dict()
        self.suspect = None #The person w/ the most amount of votes agains them
        self.spy = None
        self.location = None
        self.game_msg = None
        self.voice_channel = None
    async def display(self):
        embed = discord.Embed(title="Spyfall", description="~Courtesy of Redux", color=0x00ff00)
        playerList = ""
        for player in self.players.keys():
            playerList += player.display_name + ":" + str(self.players[player]) + ", "
        playerList = playerList[:-2]

        status = ""
        if self.state == 1:
            status = "Use `$spyfall vote <@Player>` if you think they are the spy.\nYou may only use this once per round."
        elif self.state == 2:
            status = "The round is over! The spy has lost, it was: \n " + self.spy.display_name
        elif self.state == 3:
            status = "The round is over! The spy has won, it was: \n " + self.spy.display_name
        embed.add_field(name="Status", value=status, inline=False)

        self.updateSuspect()
        suspect = "..."
        if self.suspect != None:
            suspect = self.suspect.display_name + " - " + str(self.players[self.suspect]) + " vote(s)"
        embed.add_field(name="Suspect", value=suspect, inline=False)
        embed.add_field(name="Players", value=playerList, inline=False)
        await self.bot.edit_message(self.game_msg, new_content = ".", embed=embed)
    async def displayLocations(self, channel):
        embed = discord.Embed(title="Spyfall Locations", description="~Courtesy of Redux", color=0xff0000)
        message = ""
        locations = list(self.config['locations']);
        length = len(locations)
        for i in range(0, int(length/2)):
            message += locations[i] + "\n"
        embed.add_field(name="-", value=message, inline=True)

        message = ""
        for i in range(int(length/2), length):
            message += locations[i] + "\n"
        embed.add_field(name="-", value=message, inline=True)

        await self.bot.send_message(channel, embed=embed)
    def updateSuspect(self):
        #Find the most voted person
        print(self.players.values())

        votes = -1
        for key, value in self.players.items():
            if value > votes:
                self.suspect = key
                votes = value
            elif value == votes:
                self.suspect = None

        print(self.players.values())
    async def votesIn(self):
        self.updateSuspect()
        if self.suspect == self.spy:
            self.state = 2
        else:
            self.state = 3
        await self.display()


    @commands.group(pass_context=True)
    async def spyfall(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,
                                        "Please use a subcommand, view the link below for more information.\nhttps://github.com/PanjaCo/Redux-Bot/")
        else:
            await self.bot.delete_message(ctx.message)
    @spyfall.command(pass_context = True)
    async def new(self, ctx):
        if ctx.message.author.voice:
            self.reset()
            self.state = 1
            self.voice_channel = ctx.message.author.voice.voice_channel
            self.game_msg = await self.bot.send_message(ctx.message.channel, "Setting up the game...")

            lPlayers = self.voice_channel.voice_members
            for player in lPlayers:
                self.players[player] = 0
            await self.displayLocations(ctx.message.channel)
            await self.display()
            self.location = list(self.config['locations'])[randint(0, len(self.config['locations'])-1)]
            self.spy = list(self.players.keys())[randint(0, len(self.players)-1)]

            #DM the location to everyone but the spy
            for player in self.players.keys():
                if player != self.spy:
                    await self.bot.send_message(player, "You are at a(n) " + self.location)
                else:
                    await self.bot.send_message(player, "You are the spy!\nTry to blend in and figure out where you are.\nUse `$spyfall guess <location>` once you are sure, you only have one guess.")
            await self.display()
    @spyfall.command(pass_context = True)
    async def guess(self, ctx):
        if self.state != 1:
            await self.bot.send_message(ctx.message.channel, "There is not a round in progress")
            return
        if ctx.message.author != self.spy:
            await self.bot.send_message(ctx.message.channel, "You are not the spy, you can not use this command.")
            return

        args = (ctx.message.content).split()[2:]
        location = (" ").join(args)
        if self.location.lower() == location.lower():
            self.state = 3
        else:
            self.state = 2
        await self.display()
    @spyfall.command(pass_context = True)
    async def vote(self, ctx, suspect:discord.Member):
        if self.state != 1:
            await self.bot.send_message(ctx.message.channel, "There is not a round in progress")
            return

        for player in self.voted:
            if player == ctx.message.author:
                await self.bot.send_message(ctx.message.channel, "You have already voted")
                return
        found = False
        for player in self.players.keys():
            if player == suspect:
                self.players[player] += 1
                self.voted.append(ctx.message.author)
                found = True
        if not found:
            await self.bot.send_message(ctx.message.channel, "Player not found")
            return
        #Check if every player has voted
        if len(self.players) == len(self.voted):
            await self.votesIn()
        else:
            self.updateSuspect()
            await self.display()
    @spyfall.command(pass_context = True)
    async def timesup(self, ctx):
        if self.state != 1:
            await self.bot.send_message(ctx.message.channel, "There is not a round in progress")
            return
        self.state = 3
        await self.display()



def setup(bot):
    try:
        bot.add_cog(Spyfall(bot, config.spyfall))
        print("[Spyfall Module Loaded]")
    except Exception as e:
        print(" >> Spyfall Module: {0}".format(e))