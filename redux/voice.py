import asyncio
import discord
from discord.ext import commands
import time

#Discord API
discordToken = 'MzkwNjQzODc0OTQ4NzEwNDAw.DRR4Ww.9T8nLs1Qf75Pec5xHIW-H-A_UTo';
client = discord.Client()
#conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='music', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

class Music:
    def __init__(self, client):
        self.client = client
        self.voice = None
        self.player = None
        self.volume = 1.0
        #self.playlist = playlist.Queue()
        self.seconds_to_next = 0
        self.music_server = None
    async def create_voice_client(self, channel):
        voice = await self.client.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice
    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        ''' Joins the voice channel of the message author '''
        targetChannel = ctx.message.author.voice_channel
        self.channel = targetChannel
        self.textChannel = ctx.message.channel
        if self.voice:
            if self.voice.channel.id == ctx.message.author.voice.voice_channel.id:
                await self.client.say("I'm already here ya dingus")
            else:
                await self.voice.move_to(ctx.message.author.voice.voice_channel)
                self.music_server = self.voice_channel
        else:
            self.voice = await self.client.join_voice_channel(ctx.message.author.voice.voice_channel)
            self.music_server = self.voice
    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, songId: str):
        self.currentSong = "files/" + songId + ".mp3"
        self.player = self.music_server.create_ffmpeg_player(self.currentSong)
        self.player.start()
        await self.client.send_message(self.textChannel, "BIG NIGS!")
    @commands.command(pass_context=True, no_pm=True)
    async def disconnect(self, ctx):
        self.client.disconnect()
                
#
client = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='A playlist example for discord.py')
client.add_cog(Music(client))

@client.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(client.user))

client.run(discordToken)
