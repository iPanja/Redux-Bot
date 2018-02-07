import discord
from discord.ext import commands
from random import shuffle
import time

class Blackjack:
    def __init__(self, bot):
        self.bot = bot;
        self.setup();

    def setup(self):
        self.deck = [];
        self.deck = self.newDeck();
        self.pHand = [];
        self.dHand = [];
        self.state = 0;  # 1=Player, 2=Dealer, 3=GameOver
        self.assignHands();

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

    def printHands(self):
        for i in range(0, 10):
            print("\n");

        print("You: " + str(self.calc(self.pHand)));
        msg = "";
        for card in self.pHand:
            msg += (card + ", ");
        print(msg)

        msg = "";
        if (self.state == 1):
            for card in self.dHand:
                msg += (card + ", ");
            print("\nDealer: " + str(self.calc(self.dHand)));
            print(msg);
        else:
            print("\nDealer: ");
            print(self.dHand[0] + ", ?");
        print("----------------------");

    def hit(self, hand):
        hand.append(self.deck[0]);
        self.deck.pop(0);
    def display(self, msg):
        msg += "Your Hand: " + str(self.calc(self.pHand)) + "\n";
        for card in self.pHand:
            msg += (card + ", ");
        msg += "\nDealer's Hand: " + str(self.calc(self.dHand)) + "\n";
        if(self.state == 1):
            msg += "?";
        else:
            for card in self.dHand:
                msg += (card + ", ");
        return msg;

    @commands.command(pass_context=True)
    @commands.cooldown(1, 2, commands.BucketType.server)
    async def blackjack(self, ctx, choice:str):
        if(choice == "create"):
            self.setup();
            msg = "New game setup vs AI Dealer.\n\n";
            await self.bot.send_message(ctx.message.channel, self.display(msg));
        elif(choice == "hit" or choice == "1"):
            self.hit(self.pHand);
            calc = self.calc(self.pHand);

            msg = self.display("") + "\n";
            if(calc > 21):
                await self.bot.send_message(ctx.message.channel, msg + "Blackjack: Game over, you have lost.")
                self.state = 2;
            elif(calc == 21):
                await self.bot.send_message(ctx.message.channel, msg + "Nice, 21 exactly - Advancing to Dealer's Turn");
                self.state = 1;
            else:
                await self.bot.send_message(ctx.message.channel, msg);
        elif(choice == "stay" or choice == "2"):
            while(self.state != 2):
                dCalc = self.calc(self.dHand);
                if(dCalc <= 16):
                    self.hit(self.dHand);
                    time.sleep(2);
                else:
                    gWinner = self.winner();
                    msg = self.display("") + "\n";
                    if(gWinner == 0):
                        await self.bot.send_message(ctx.message.channel, msg + "Blackjack: Game over, you have won.");
                    elif(gWinner == 1):
                        await self.bot.send_message(ctx.message.channel, msg + "Blackjack: Game over, you have lost.");
                    else:
                        await self.bot.send_message(ctx.message.channel, msg + "Blackjack: Game over, you have tied.");
                    self.state = 2;

def setup(bot):
    try:
        bot.add_cog(Blackjack(bot))
        print("[Blackjack Module Loaded]")
    except Exception as e:
        print(" >> Blackjack Module: {0}".format(e))