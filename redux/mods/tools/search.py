import json
import difflib

#Json -> Dict
dict = []
with open('weapon_data.files', 'r') as f:
    dict = json.load(f)

print(dict)
keys = list(dict.keys())

query = "Uncommon assault rifle";

match = (difflib.get_close_matches(query, keys))
print(match)

if(len(match) > 0):
    print(dict[match[0]])
