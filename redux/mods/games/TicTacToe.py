import discord
from discord.ext import commands
import time, math
from pprint import pprint

class TicTacToe:
    def __init__(self, bot):
        self.bot = bot
        self.reset()
    def reset(self):
        self.state = 0  # 0 = Gameover, 1 = Player 1's Turn, 2 = Player 2's Turn
        self.board = [[0 for x in range(3)] for y in range(3)]
        self.p1 = None
        self.p2 = None
        self.winner = None
        self.game_channel = None
        self.game_msg = None
    def _horizontal(self, turn):
        for column in self.board:
            broke = False
            for piece in column:
                if piece != turn:
                    broke = True
                    break
            if not broke:
                return True
        return False
    def _vertical(self, turn):
        for r in range(0, 2): #Vertical Column
            broke = False
            for c in range(0, 2): #Row Piece
                if self.board[c][r] != turn:
                    broke = True
                    break
            if not broke:
                return True
        return False
    def _diagonal(self, turn):
        if self.board[0][0] == turn and self.board[1][1] == turn and self.board[2][2]:
            return True
        if self.board[2][0] == turn and self.board[1][1] == turn and self.board[0][2]:
            return True
        return False

    async def display(self):
        embed = discord.Embed(title="Tic Tac Toe", description='\U0001f1fd ' + self.p1.display_name + " vs \U0001f17e  " + self.p2.display_name, color=0x00ff00)
        text = ""
        counter = 1
        prev = False
        for row in self.board:
            for piece in row:
                if piece == 0:
                    text += str(counter)
                    prev = True
                elif piece == 1:
                    text += '\U0001f1fd'
                else:
                    text += '\U0001f17e'
                text += ' '
                if prev:
                    text += "   "
                    prev = False
                counter += 1
            text += "\n"
        status = "Player " + str(self.state) + "'s turn."
        if self.state == 0:
            status = "Game Over."
        elif self.winner != None:
            self.state = 0
            status = "Game Over. The winner is "
            if self.winner == self.p1:
                status += "\U0001f1fd " + self.p1.display_name
            else:
                status += "\U0001f17e " + self.p2.display_name
        embed.add_field(name="Board", value=text)
        embed.add_field(name="Status", value=status, inline=False)
        self.game_msg = await self.bot.edit_message(self.game_msg, new_content = ".", embed = embed)
    @commands.group(pass_context=True)
    async def ttt(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,
                                        "Please use a subcommand, view the link below for more information.\nhttps://github.com/PanjaCo/Redux-Bot/")
        else:
            await self.bot.delete_message(ctx.message)

    @ttt.command(pass_context = True)
    async def new(self, ctx, p1:discord.Member, p2:discord.Member):
        if self.state != 0:
            await self.bot.send_message(ctx.message.channel, "A game is already running, please use the following command if you wish to proceed. ```$ttt remake```")
            return
        self.reset()
        self.state = 1
        self.game_channel = ctx.message.channel
        self.game_msg = await self.bot.send_message(self.game_channel, "The game is being setup...")
        self.p1 = p1
        self.p2 = p2
        time.sleep(3)
        await self.display()
    @ttt.command(pass_context = True)
    async def remake(self, ctx):
        self.reset()
        await self.bot.send_message(ctx.message.channel, "The game has been reset, please use the following command. ```$ttt new <@Player1> <@Player2>```")
    @ttt.command(pass_context = True)
    async def place(self, ctx, position:int):
        if self.state == 0:
            return
        if position < 1 or position > 9:
            return
        if self.state == 1 and self.p1 != ctx.message.author:
            return
        if self.state == 2 and self.p2 != ctx.message.author:
            return

        column = int((position - 1) / 3)
        row = (position - 1) - (column * 3)

        if self.board[column][row] == 0:
            if self.state == 1:
                self.board[column][row] = 1
                if self._horizontal(self.state) or self._vertical(self.state) or self._diagonal(self.state):
                    self.winner = self.p1
                self.state = 2
            else:
                self.board[column][row] = 2
                if self._horizontal(self.state) or self._vertical(self.state) or self._diagonal(self.state):
                    self.winner = self.p2
                self.state = 1
        else:
            await self.bot.send_message(ctx.message.channel, "You can not place your chip here")
            return
        await self.display()






def setup(bot):
    try:
        bot.add_cog(TicTacToe(bot))
        print("[TicTacToe Module Loaded]")
    except Exception as e:
        print(" >> TicTacToe Module: {0}".format(e))