import discord
from discord.ext import commands

class Connect4:
    def __init__(self, bot):
        self.bot = bot
        self.reset()
    def reset(self):
        self.game_msg = None
        self.game_channel = None
        self.p1 = None
        self.p2 = None
        self.state = 0 #0 = GameOver, 1 = Player 1, 2 = Player Two
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.winner = None

    @commands.group(pass_context = True)
    async def c4(self, ctx):

        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel, "Please use a subcommand, view the link below for more information.\nhttps://github.com/PanjaCo/Redux-Bot/")
        else:
            await self.bot.delete_message(ctx.message)

    @c4.command(pass_context = True)
    async def new(self, ctx, p1:discord.Member, p2:discord.Member):
        if self.state != 0:
            await self.bot.send_message(ctx.message.channel, "A game is currently in progress, please use ```$c4 remake``` if you wish to proceed.")
            return
        self.reset()
        self.p1 = p1
        self.p2 = p2
        self.state = 1
        self.game_channel = ctx.message.channel
        self.game_msg = await self.bot.send_message(self.game_channel, "The game is being setup...")
        await self.display()
    @c4.command(pass_context = True)
    async def remake(self, ctx):
        self.reset()
        await self.bot.send_message(ctx.message.channel, "You may now use ```$c4 create <@player> <@player>``` to create a new game.")
    @c4.command(pass_context = True)
    async def place(self, ctx, x:int):
        if self.state == 0:
            return
        if self.state == 1 and self.p1 != ctx.message.author:
            return
        if self.state == 2 and self.p2 != ctx.message.author:
            return

        x -= 1
        y = 0

        placed = False
        for iy in range(5, -1, -1):
            if self.board[iy][x] == 0:
                self.board[iy][x] = self.state
                placed = True
                y = iy
                break

        if placed:
            if not self.checkWin(x, y, self.state):
                if self.state == 1:
                    self.state = 2
                else:
                    self.state = 1
            await self.display()

    async def display(self):
        embed = discord.Embed(title="Connect 4", description='\N{large red circle} ' + self.p1.display_name + " vs \N{large blue circle} " + self.p2.display_name)
        text = ".  1 \t2  \t3 \t4 \t5 \t6 \t7\n"
        for row in self.board:
            for piece in row:
                if piece == 0:
                    text += '\N{medium white circle}'
                elif piece == 1:
                    text += '\N{large red circle}'
                else:
                    text += '\N{large blue circle}'
            text += "\n"
        embed.add_field(name="Board", value=text)

        status = "Game Over"
        if self.state == 1:
            status = "\N{large red circle} Player 1's turn"
        elif self.state == 2:
            status = "\N{large blue circle} Player 2's turn"
        elif self.winner != None:
            status += ". Player " + str(self.winner) + " has won. "
            if self.winner == 1:
                status += '\N{large red circle}'
            else:
                status += '\N{large blue circle}'

        embed.add_field(name="Status", value=status, inline=False)
        self.game_msg = await self.bot.edit_message(self.game_msg, new_content = ".", embed=embed)


    def checkWin(self, x, y, turn):
        #print(str(self.board[y][x]))
        win = self._horizontal(y, turn) or self._vertical(x, turn) or self._diagonal(x, y, turn)
        if win:
            self.state = 0
            self.winner = turn
            return True

    def _horizontal(self, y, turn):
        p = 0
        for x in range(0, 5):
            if self.board[y][x] == turn:
                p += 1
                if p == 4:
                    return True
            else:
                p = 0
        return False
    def _vertical(self, x, turn):
        p = 0
        for y in range(0, 6):
            if self.board[y][x] == turn:
                p += 1
                if p == 4:
                    return True
            else:
                p = 0
        return False
    def _diagonal(self, x, y, turn):
        p = 0
        for o in range(-4, 4):
            try:
                if self.board[y-o][x+o] == turn:
                    p += 1
                    if p == 4:
                        return True
                else:
                    p = 0
            except IndexError:
                pass
        return False

def setup(bot):
    try:
        bot.add_cog(Connect4(bot))
        print("[Connect4 Module Loaded]")
    except Exception as e:
        print(" >> Connect4 Module: {0}".format(e))