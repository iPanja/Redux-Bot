import urllib3, json
from bs4 import BeautifulSoup

url = "https://fortnitestats.net/weapons"

http = urllib3.PoolManager()
response = http.request('GET', url)
soup = BeautifulSoup(response.data)


""" Text File
with open('weapon_data.txt', 'w') as f:
    for tr in soup.find_all('tr')[2:]:
        tds = tr.find_all('td')
        f.write("Name: %s, Type: %s, Rarity: %s, Damage: %s, DPS: %s, MagSize: %s\n" % (tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text))
"""

""" JSON File """
data = dict()
for tr in soup.find_all('tr')[1:]:
    tds = tr.find_all('td')
    stats = dict()
    stats["type"] = tds[1].text
    stats["rarity"] = tds[2].text
    stats["damage"] = tds[3].text
    stats["dps"] = tds[4].text
    stats["mag_size"] = tds[5].text
    data[tds[0].text] = stats

with open('weapon_data.json', 'w') as f:
    #json.dump(data, f) --Non pretty
    #Pretty:
    f.write(json.dumps(data, sort_keys=True, indent=4))