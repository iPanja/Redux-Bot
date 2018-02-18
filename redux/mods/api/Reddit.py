import discord, praw, asyncio
from discord.ext import commands
import config

from pprint import pprint

class Reddit:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.praw = praw.Reddit(
            client_id = self.config['client_id'],
            client_secret = self.config['client_secret'],
            username = self.config['username'],
            password = self.config['password'],
            user_agent = self.config['user_agent']
        )
    @commands.command(pass_context = True)
    async def rLatest(self, ctx):
        query = "".join((ctx.message.content).split()[1:])
        submission = list(self.praw.subreddit(query).new(limit=1))[0]
        if submission.over_18:
            await self.bot.send_message(ctx.message.channel, "Sorry, but Redux has blocked this post due to sensitive-content (18+).")
            return
        embed = discord.Embed(title=query + " subreddit", description="Newest post", color=0x00ff00)
        await self.display(submission, embed, ctx.message.channel)
    @commands.command(pass_context = True)
    async def rHottest(self, ctx):
        query = "".join((ctx.message.content).split()[1:])
        submission = list(self.praw.subreddit(query).hot(limit=1))[0]
        if submission.over_18:
            await self.bot.send_message(ctx.messasge.channel, "Sorry, but Redux has blocked this post due to sensitive-content (18+).")
            return
        embed = discord.Embed(title=query + " subreddit", description="Hottest post", color=0x00ff00)
        await self.display(submission, embed, ctx.message.channel)
    @commands.command(pass_context = True)
    async def rWatch(self, ctx):
        query = "".join((ctx.message.content).split()[1:])
        try:
            subreddit = self.praw.subreddit(query)
        except ValueError:
            await self.bot.send_message(ctx.message.channel, "Subreddit not found")
            return
        self.bot.loop.create_task(self.stalk(subreddit, ctx.message.channel))
    async def stalk(self, subreddit, channel):
        for submission in subreddit.stream.submissions():
            if submission.over_18:
                await self.bot.send_message(channel, "Sorry, but Redux has blocked this post due to sensitive-content (18+).")
                return
            embed = discord.Embed(title=subreddit.display_name, description="Newest post (stalked)", color=0x00ff00)
            await self.display(submission, embed, channel)
            break
    @commands.command(pass_context = True)
    async def aww(self, ctx):
        embed = discord.Embed(title="Brighten up your day :grinning:", description="~Courtesy of Redux", color=0x00ff00)
        for submission in self.praw.subreddit("aww").hot(limit=10):
            if self.ext(submission.url):
                embed.set_image(url=submission.url)
                break

        await self.bot.send_message(ctx.message.channel, embed=embed)
    async def display(self, submission, embed, channel):
        if('imgur' in submission.url):
            #External image, display link and let Discord do the rest
            await self.bot.send_messsage(channel, submission.url)
            return
        if self.ext(submission.url):
            embed.set_image(url=submission.url)
            await self.bot.send_message(channel, embed=embed)
            return

        if len(submission.selftext) > 200:
            submission.selftext = submission.selftext[:200] + "\n..."

        embed.add_field(name="Author", value=submission.author.name)
        embed.add_field(name="Karma", value=submission.score)
        embed.add_field(name=submission.title, value=submission.selftext)
        embed.add_field(name="View post", value=submission.url)
        try:
            await self.bot.send_message(channel, embed=embed)
        except discord.errors.HTTPException:
            pprint(vars(submission))
            print("---")

    def ext(self, url):
        extensions = {'.png', '.jpg', '.jpeg'}
        for ext in extensions:
            if ext in url:
                return True
        return False

def setup(bot):
    try:
        bot.add_cog(Reddit(bot, config.reddit))
        print("[Reddit Module Loaded]")
    except Exception as e:
        print(" >> Reddit Module: {0}".format(e))