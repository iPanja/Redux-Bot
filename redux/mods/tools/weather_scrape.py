import json
from pprint import pprint

dict = []
with open('weather.json', 'r') as f:
    dict = json.load(f)

#pprint(dict)
print(dict['name'])
print(dict['sys']['country'])
print(dict['main']['temp'])