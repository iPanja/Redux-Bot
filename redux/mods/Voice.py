from __future__ import unicode_literals
import discord, asyncio, youtube_dl, pathlib, os
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

""" Youtube Download Options """
yt_config = {
    'outtmpl' : 'C:\\Users\Fletcher-Razer\Documents\Python\\redux\music\%(id)s-%(title)s.%(ext)s',
    'restrictfilenames' : True,
    'noplaylist' : True,
    'nocheckcertificate': True,
    'quiet' : True,
    'no_warnings' : True,
    'default_search' : 'auto',
    'source_address': '0.0.0.0'
}

class Voice:
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.player = None
        self.volume = 1.0
        self.voice_channel = None
        self.downloader = Downloader()

    @commands.command(pass_context = True)
    async def summon(self, ctx):
        if not ctx.message.author.voice:
            await self.bot.send_message("You are not in a voice channel.")
            return
        self.voice_channel = ctx.message.author.voice.voice_channel
        if self.bot.is_voice_connected(ctx.message.server):
            await self.bot.voice_client.move_to(self.voice_channel)
        else:
            await self.bot.join_voice_channel(self.voice_channel)

    @commands.command(pass_context = True)
    async def disconnect(self, ctx):
        for server in self.bot.voice_clients:
            if(server.server == ctx.message.server):
                return await server.disconnect()

    @commands.command(pass_context = True)
    async def play(self, ctx):
        await self.bot.add_reaction(ctx.message, '\N{HOURGLASS}')

        args = (ctx.message.content).split()[1:]
        query = (" ").join(args)
        self.downloader.fromLink(query);

        await self.bot.send_message(ctx.message.channel, "The file should be downloading...")

class Downloader:
    def __init__(self, target_directory=None):
        self.num = 0 #idk ;)

    @property
    def ytdl(self):
        return self.safe_ytdl

    @asyncio.coroutine
    def fromLink(self, url):
        with youtube_dl.YoutubeDL(yt_config) as dl:
            print(url)
            dl.download([url]);
            print("--Done--")


def setup(bot):
    try:
        bot.add_cog(Voice(bot))
        print("[Voice Module Loaded]")
    except Exception as e:
        print(" >> Voice Module: {0}".format(e))