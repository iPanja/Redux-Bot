import time
import discord
from discord.ext import commands
from random import randint
import config

class Moderation():
    def __init__(self, bot, config):
        self.bot = bot
        self.word_blacklist = config["word_blacklist"]
        self.memelist = config["memelist"]
    def isBlacklisted(self, message):
        for bWord in self.word_blacklist:
            if bWord in message.content.lower():
                return True
        return False
    def getMeme(self):
        index = randint(-1, len(self.memelist))
        meme = self.memelist[index-1]
        return meme

    @commands.command(pass_context = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def clean(self, ctx, max_messanges:int = 50):
        if(not isinstance(max_messanges, int)):
            return
        if(max_messanges >= 150):
            await self.bot.send_message(ctx.message.channel, "You can only delete up to 150 messages at a time")
            return

        messages = []
        async for x in self.bot.logs_from(ctx.message.channel, limit=max_messanges):
            messages.append(x)
        await self.bot.delete_messages(messages)
        await self.bot.send_message(ctx.message.channel, "=== Deletion Completed ===")
    @commands.command(pass_context = True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def spam(self, ctx, msg:str, max:int = 5):
        for i in range(0, max):
            await self.bot.send_message(ctx.message.channel, msg)
            time.sleep(1);
    async def scrub(self, message):
        isBlocked = self.isBlacklisted(message)
        if (isBlocked):
            """await self.bot.delete_messages([message])"""
            await self.bot.delete_message(message)
            meme = self.getMeme()
            await self.bot.send_message(message.channel, meme + " -Courtesy of Roblox Admin Team")

from pprint import pprint
def setup(bot):
    try:
        bot.add_cog(Moderation(bot, config.moderation))
        print("[Moderation Module Loaded]")
    except Exception as e:
        print(" >> Moderation Module: {0}".format(e))