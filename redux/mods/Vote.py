import discord
from discord.ext import commands

class Vote:
    def __init__(self, bot):
        self.bot = bot
        self.name = ""
        self.index = 1
        self.options = list()
    @commands.command(pass_context = True)
    async def pcreate(self, ctx):
        args = (ctx.message.content).split()[1:]
        self.name = (" ").join(args)

        await self.bot.send_message(ctx.message.channel, "The poll, '" + self.name + "' has been created.\nUse $poption <option> to create an option for the poll.\nThen use $cstart to start the poll.")
    @commands.command(pass_context = True)
    async def poption(self, ctx):
        args = (ctx.message.content).split()[1:]
        option = (" ").join(args)

        voteOption = VoteOption(self.index, option)
        self.index += 1;
        self.options.append(voteOption)

        await self.bot.delete_message(ctx.message)
        await self.bot.send_message(ctx.message.channel, "New option added, '" + option + ".'")
    @commands.command(pass_context = True)
    async def pstart(self, ctx):
        channel = ctx.message.channel
        await self.bot.send_message(ctx.message.channel, "The poll has now started.");
    @commands.command(pass_context = True)
    async def pvote(self, ctx, index:int):
        for option in self.options:
            if option.getNum() == index:
                option.vote()
        await self.bot.delete_message(ctx.message)
        await self.bot.send_message(ctx.message.channel, "Thank you, your vote has been recorded.")
    @commands.command(pass_context = True)
    async def pstop(self, ctx):
        msg = "'" + self.name + "' has ended. results:\n"
        winnerName = ""
        winnerVotes = 0
        tie = False
        tieOptions = list()
        for option in self.options:
            if option.getVotes() > winnerVotes:
                winnerVotes = option.getVotes()
                winnerName = option.getName()
            elif option.getVotes() == winnerVotes:
                if not tie:
                    tieOptions.append(winnerName)
                tie = True
                tieOptions.append(option.getName())
            msg += "  " + str(option.getNum()) + ". " + option.getName() + " - " + str(option.getVotes()) + " votes.\n"
        if tie:
            msg += "\nTie! Winners:\n"
            for winner in tieOptions:
                msg += "  " + winner + "\n"
            msg += "with " + str(winnerVotes) + " votes."
        else:
            msg += "\nWinner: '" + winnerName + "' with " + str(winnerVotes) + " votes."
        await self.bot.send_message(ctx.message.channel, msg)
        self.resetVote()
    @commands.command(pass_context = True)
    async def pcurrent(self, ctx):
        msg = "Poll: " + self.name + "\n"
        msg = self.getOptions(msg)
        await self.bot.send_message(ctx.message.channel, msg)
    def getOptions(self, msg):
        for option in self.options:
            msg += "  " + str(option.getNum()) + ". " + option.getName() + "\n"
        return msg

    def resetVote(self):
        self.name = ""
        self.options = list()
        self.index = 1

class VoteOption:
    def __init__(self, num, name):
        self.num = num
        self.name = name
        self.votes = 0
    def vote(self):
        self.votes += 1
    def getVotes(self):
        return self.votes
    def getName(self):
        return self.name
    def getNum(self):
        return self.num

def setup(bot):
    try:
        bot.add_cog(Vote(bot))
        print("[Vote Module Loaded]")
    except Exception as e:
        print(" >> Vote Module: {0}".format(e))