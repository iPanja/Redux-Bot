import discord
from discord.ext import commands
from random import shuffle
import time

class Blackjack:
    def __init__(self, bot):
        self.bot = bot;
        self.state = 3

    def setup(self):
        self.deck = []
        self.deck = self.newDeck()
        self.pHand = []
        self.dHand = []
        self.game_msg = None
        self.game_channel = None
        self.state = 1  # 1=Player, 2=Dealer, 3=GameOver, 4=CalcWinner
        self.assignHands()

    @staticmethod
    def newDeck():
        nDeck = [];
        for suit in ["H", "D", "S", "C"]:
            for card in [2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K"]:
                nDeck.append(suit + str(card));
        shuffle(nDeck);
        return nDeck;

    def assignHands(self):
        for hand in [self.pHand, self.dHand]:
            for i in range(0, 2):
                hand.append(self.deck[0]);
                self.deck.pop(0);

    @staticmethod
    def calc(hand):
        total = 0;
        for card in hand:
            try:
                total += int(card[1])
            except ValueError:
                if (card[1] in ["T", "J", "Q", "K"]):
                    total += 10;
                elif (card[1] == "A"):
                    if (not (total + 11 > 21)):
                        total += 11;
                    else:
                        total += 1;
                else:
                    print("Card Type Error")
        return total;

    def winner(self):
        pCalc = self.calc(self.pHand);
        dCalc = self.calc(self.dHand);
        if (pCalc > 21):
            return 1;
        elif (dCalc > 21):
            return 0;
        elif (pCalc > dCalc):
            return 0;
        elif (dCalc > pCalc):
            return 1;
        elif (pCalc == dCalc):
            return 2;
        else:
            print("winner: error");

    def hit(self, hand):
        hand.append(self.deck[0]);
        self.deck.pop(0);

    async def display(self):
        embed = discord.Embed(title="Blackjack", description="You vs AI", color=0x00ff00)

        temp = ""
        for card in self.pHand:
            temp += card + ", "
        embed.add_field(name="Your Hand: " + str(self.calc(self.pHand)), value=temp)

        temp = ""
        calc = ""
        if self.state == 1:
            temp = self.dHand[0] + ", ?"
            calc = "?"
        else:
            for card in self.dHand:
                temp += card + ", "
                calc = str(self.calc(self.dHand))

        embed.add_field(name="Dealer's Hand: " + calc, value=temp)

        temp = ""
        if self.state == 1:
            temp = "Select an option"
        elif self.state == 2:
            temp = "The dealer is taking his turn..."
        elif self.state == 4:
            self.state = 3
            temp = "Game Over - You have "
            if self.winner() == 0:
                temp += "won"
            elif self.winner() == 1:
                temp += "lost"
            else:
                temp += "tied"
        else:
            temp = "ERROR, uh..."


        embed.add_field(name="Status", value=temp, inline=False)

        self.game_msg = await self.bot.edit_message(self.game_msg, new_content=".", embed=embed)

        if(self.state == 3):
            self.game_msg = None
    @commands.command(pass_context=True)
    @commands.cooldown(1, 2, commands.BucketType.server)
    async def blackjack(self, ctx, choice:str):
        if(choice == "create"):
            if self.state != 3:
                await self.bot.send_message(ctx.message.channel, "A game is currently in progress... use '$blackjack reset' to confirm this action")
                return
            self.setup()
            self.game_channel = ctx.message.channel
            self.game_msg = await self.bot.send_message(ctx.message.channel, "The game is being created...")
            time.sleep(2)

            await self.display()
        elif(choice == "hit" or choice == "1") and self.state == 1:
            self.hit(self.pHand);
            if self.calc(self.pHand) > 21:
                self.state = 4
            await self.display()
        elif(choice == "stay" or choice == "2") and self.state == 1:
            while(self.state != 3):
                dCalc = self.calc(self.dHand);
                if(dCalc <= 16):
                    self.hit(self.dHand)
                else:
                    self.state = 4;
                await self.display()
        elif(choice == "reset"):
            self.setup()
            self.game_channel = ctx.message.channel
            self.game_msg = await self.bot.send_message(ctx.message.channel, "The game is being created...")
            time.sleep(2)

            await self.display()
        #Cleanup Command
        await self.bot.delete_message(ctx.message)

def setup(bot):
    try:
        bot.add_cog(Blackjack(bot))
        print("[Blackjack Module Loaded]")
    except Exception as e:
        print(" >> Blackjack Module: {0}".format(e))