import discord, asyncio, threading
from discord.ext import commands
from random import *
import config

from pprint import pprint

class Hangman:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.state = 0
        self.reset()
    def reset(self):
        self.state = 0
        self.word = None
        self.hidden = None
        self.game_channel = None
        self.game_message = None
        self.lives = None
        self.guesses = list()
    def genHidden(self, word: str):
        hidden = ""
        for letter in list(word):
            if letter == " ":
                hidden += " ."
            else:
                hidden += "- "
        return "".join(hidden)
    def _guess(self, letter: str):
        temp = list(self.hidden)
        correct = False
        for index in range(0, len(self.word)):
            if letter == self.word[index]:
                temp[(index * 2)] = letter
                correct = True
        self.hidden = "".join(temp)
        self.guesses.append(letter)
        if not correct:
            self.lives -= 1
    async def display(self):
        embed = discord.Embed(title="Hangman", description="~Courtesy of Redux", color=0x00ff00)

        hearts_label = ". "
        for i in range(0, self.lives):
            hearts_label += ":heart: "

        guesses_label = ". "
        for g in self.guesses:
            guesses_label += g + " "

        status = "Guess a letter."
        if self.lives == 0:
            status = "Game Over. You have lost"
            self.hidden = ""
            for letter in list(self.word):
                self.hidden += letter + " "
        elif not "-" in self.hidden:
            status = "Game Over. You have won!"
            self.state = 0

        embed.add_field(name="Life", value=hearts_label, inline=False)
        embed.add_field(name="Word", value=self.hidden, inline=False)
        embed.add_field(name="Guesses", value=guesses_label, inline=False)
        embed.add_field(name="Status", value=status, inline=False)
        await self.bot.edit_message(self.game_message, new_content=".", embed=embed)
    @commands.group(pass_context=True)
    async def hangman(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel, "Please use a subcommand, view the link below for more information.\nhttps://github.com/PanjaCo/Redux-Bot/")
        else:
            await self.bot.delete_message(ctx.message)

    @hangman.command(pass_context = True)
    async def new(self, ctx):
        if self.state != 0:
            await self.bot.send_message(ctx.message.channel, "A game is currently in progress, use ```$hangman remake``` to confirm this action.")
            return
        self.reset()
        self.state = 1

        args = (ctx.message.content).split()
        if(len(args) > 2):
            query = " ".join(args[2:])
            self.word = query.lower()
        else:
            self.word = list(self.config['wordlist'])[randint(0, len(self.config['wordlist'])-1)]
        self.hidden = self.genHidden(self.word)
        self.lives = 6
        self.game_channel = ctx.message.channel
        self.game_message = await self.bot.send_message(self.game_channel, "The game is being setup...")
        await self.display()

    @hangman.command(pass_context = True)
    async def guess(self, ctx, letter:str):
        letter = letter.lower()
        if self.state == 0:
            await self.bot.send_message(ctx.message.channel, "There is no active Hangman game currently, use ```$hangman new``` to create one.")
            return
        elif len(letter) != 1:
            await self.bot.send_message(ctx.message.channel, "Your input should only be 1 character.")
            return
        elif letter in self.guesses:
            await self.bot.send_message(ctx.message.channel, "You have already guessed that letter.")
            return
        self._guess(letter)
        await self.display()

    @hangman.command(pass_context = True)
    async def remake(self, ctx):
        if self.state == 0:
            await self.bot.send_message(ctx.message.channel, "There is no active Hangman game currently, use ```$hangman new``` to create one.")
            return
        self.reset()
        await self.bot.send_message(ctx.message.channel, "Please use ```$hangman new``` now")
def setup(bot):
    try:
        bot.add_cog(Hangman(bot, config.hangman))
        print("[Hangman Module Loaded]")
    except Exception as e:
        print(" >> Hangman Module: {0}".format(e))