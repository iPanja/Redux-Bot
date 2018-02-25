cards_rank = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
heirarchy = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind",
             "Straight Flush", "Royal Flush"]

class Hand:
    def __init__(self, string):
        self.cards = list()
        self.suits = list()
        for i in range(0, 13, 3):
            self.cards.append(string[i])
            self.suits.append(string[i + 1])

    # Get a list of duplicate cards, along with how many there are of them
    def dupes(self, group=None):
        if group == None:
            group = self.cards
        dupes = dict()
        for card in group:
            if not card in dupes.keys():
                dupes[card] = 1
            else:
                dupes[card] += 1
        for key in list(dupes.keys()):
            if dupes[key] == 1:
                dupes.pop(key, None)
        return dupes

    # (Boolean) Flush
    def flush(self):
        for value in self.dupes(group=self.suits).values():
            if value == 5:
                return True
        return False

    # (Boolean) Full House
    def fullhouse(self):
        p2 = False
        p3 = False
        for value in self.dupes().values():
            if value == 2:
                p2 = True
            elif value == 3:
                p3 = True
        if p2 and p3:
            return True
        return False

    # (Boolean) Straight
    def straight(self):
        index = None
        sort = sorted(self.cards, key=lambda x: cards_rank.index(x))
        count = 1
        for card in sort:
            temp = cards_rank.index(card)
            if index != None:
                if temp - 1 == index:
                    count += 1
            index = temp
        if sort[0] == "2" and sort[4] == "A":
            count += 1
        if count == 5:
            return True
        return False

    # (Boolean) Royal Flush
    def royalflush(self):
        if self.flush() and self.straight():
            if "T" in self.cards and "A" in self.cards:
                return True
        return False

    def calculate(self):
        calculated = [0]
        paired = False
        for key, value in self.dupes().items():
            if value == 2 and not paired:
                calculated.append(1)  # >> Pair
                paired = True
            elif value == 2 and paired:
                calculated.append(2)  # >> Two pairs
            elif value == 3:
                calculated.append(3)  # >> Three of a kind
            elif value == 4:
                calculated.append(7)  # >> Four of a kind
        if self.straight():
            calculated.append(4)  # >> Straight
        if self.flush():
            calculated.append(5)  # >> Flush
        if self.fullhouse():
            calculated.append(6)  # >> Full House
        if self.straight() and self.flush():
            calculated.append(8)  # >> Straight flush
        if self.royalflush():
            calculated.append(9)  # >> Royal flush
        return max(calculated)


class Comparison:
    def __init__(self, string1, string2):
        self.one = Hand(string1)
        self.two = Hand(string2)

    def compare(self):
        oC = self.one.calculate()
        tC = self.two.calculate()
        self.out = [oC, tC]
        if oC > tC:
            return 1
        elif oC < tC:
            return 2
        else:
            if oC == 1 or oC == 2 or oC == 3 or oC == 7 or oC == 6:
                oS = self.one.dupes()
                tS = self.two.dupes()
                index = len(oS) - 1
                oS = [(key, oS[key]) for key in sorted(oS, key=oS.get)]
                tS = [(key, tS[key]) for key in sorted(tS, key=tS.get)]
                fullhouse = (oC == 6)
                return self.compare_pairs(index, oS, tS, fullhouse)
            elif oC == 4:
                return self.highWinner()
            elif oC == 5:
                return self.highWinner()
            elif oC == 8:
                return self.highWinner()
            elif oC == 9:
                return 3
            elif oC == 0:
                return self.highWinner()

            return 666

    # Compare pairs
    def compare_pairs(self, index, oS, tS, fullhouse=False):
        if index == -1:
            if fullhouse:
                return 3
            oneH = self.high(self.one.cards)
            twoH = self.high(self.two.cards)
            o = cards_rank.index(sorted(oneH, key=lambda x: cards_rank.index(x))[-1])
            t = cards_rank.index(sorted(twoH, key=lambda x: cards_rank.index(x))[-1])
        else:
            o = cards_rank.index(oS[index][0])
            t = cards_rank.index(tS[index][0])
        if o > t:
            return 1
        elif o < t:
            return 2
        else:
            if index == -1:
                return 3
            return self.compare_pairs(index - 1, oS, tS, fullhouse)

    def high(self, group):
        group = self.dupes(group)
        sort = sorted(group, key=lambda x: cards_rank.index(x))
        return sort[len(sort) - 1]

    def dupes(self, group):
        dupes = dict()
        for card in group:
            if not card in dupes.keys():
                dupes[card] = 1
            else:
                dupes[card] = dupes[card] + 1
        for key in list(dupes.keys()):
            if dupes[key] != 1:
                dupes.pop(key, None)
        return dupes

    def highWinner(self):
        o = cards_rank.index(self.high(self.one.cards))
        t = cards_rank.index(self.high(self.two.cards))
        if o > t:
            return 1
        elif o < t:
            return 2
        else:
            return 3

with open('./p054_poker.txt') as f:
    content = f.readlines()

counter = 0
output = list()
for entry in content:
    entry.strip()
    game = Comparison(entry[:14], entry[15:])
    result = game.compare()
    if result == 1:
        counter += 1
    output.append(entry.strip() + " -=- Player " + str(result) + " -=- " + heirarchy[game.out[result-1]])
print("Player 1 has won: " + str(counter) + " times.")

with open('./output2.txt', 'w') as f:
    for entry in output:
        f.write("%s\n" % entry)