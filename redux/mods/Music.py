from __future__ import unicode_literals
import discord, asyncio, youtube_dl, threading
from discord.ext import commands

yt_config = {
    'outtmpl' : 'F:\Fletcher\Documents\GitHub\Redux-Bot\\redux\music\%(id)s.%(ext)s',
    'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    'restrictfilenames' : True,
    'noplaylist' : True,
    'nocheckcertificate': True,
    'quiet' : True,
    'no_warnings' : True,
    'default_search' : 'auto',
    'source_address': '0.0.0.0'
}

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.queue = list()
        self._connected = False
        self.vol = 0.5
        self.player = None
    @commands.command(pass_context = True)
    async def summon(self, ctx):
        await self._summon(ctx)
    async def _summon(self, ctx):
        if not ctx.message.author.voice:
            await self.bot.send_message(ctx.message.channel, "You are not in a voice channel.")
            return
        self.voice_channel = ctx.message.author.voice.voice_channel
        if self.bot.is_voice_connected(ctx.message.server):
            self.voice = await self.bot.voice_client.move_to(self.voice_channel)
        else:
            self.voice = await self.bot.join_voice_channel(self.voice_channel)
        self._connected = True
    @commands.command(pass_context = True)
    async def play(self, ctx, song:str):
        #   => Check if the bot is connected, if not connect
        if not self._connected:
            print("auto connect")
            await self._summon(ctx)

        #   => If a song is playing, add the request to the queue
        if(len(self.queue) > 0):
            self.queue.append(song)
            return

        #   => If no songs are playing, play this request
        self.queue.append(song)
        self.player = await self.voice.create_ytdl_player(song, ytdl_options=yt_config, after=self.next)
        self.player.start()
        self.player.volume = self.vol

    def _next(self):
        print("kkkkkkkkkk")
        if self.player.is_playing:
            return
        if not self._connected:
            return
        self.queue.pop(0)
        if len(self.queue) == 0:
            return



    @commands.command(pass_context = True)
    async def disconnect(self, ctx):
        for server in self.bot.voice_clients:
            if(server.server == ctx.message.server):
                return await server.disconnect()

        if self.player.is_playing():
            self.player.stop()

        self._connected = False

    @commands.command(pass_context = True)
    async def volume(self, ctx, value:float):
        if not self._connected:
            return

        if value > 1:
            value = 1
        elif value < 0:
            value = 0.1
        self.player.volume = value
        self.vol = value

    @commands.command()
    async def skip(self):
        if not self._connected:
            return

        self.player.stop()


def setup(bot):
    try:
        bot.add_cog(Music(bot))
        print("[Music* Module Loaded]")
    except Exception as e:
        print(" >> Music* Module: {0}".format(e))