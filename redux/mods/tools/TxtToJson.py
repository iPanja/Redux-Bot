import json
from pprint import pprint

cards = dict()

file = open("taboo_cards.txt", "r")
for line in file.readlines():
    values = line.strip().split(',')
    cards[values[0]] = list(values[1:])

with open('taboo_cards.json', 'w') as file:
    #This method (vs `json.dump(cards, file)`) will "prettify" the code so that it is NOT all on one line, crammed
    file.write(json.dumps(cards, sort_keys=True, indent=4))