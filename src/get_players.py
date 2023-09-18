import pandas as pd
import requests as rq
import re,random
ranks = ['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
tiers = ['I','II','III','IV']
def get_players(server,rank,tier,api_key):
    api_url = 'https://' +server +'.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/' +rank + '/' + tier + '?page=1&api_key=' + api_key
    players = rq.get(api_url).json()
    player_list = []
    for k in players:
        if is_alphanumeric(k['summonerName']):
            player_list.append('(' +k['summonerName'] + ',' + rank + ')')
    return player_list

def is_alphanumeric(string):
    pattern = re.compile('^([0-9a-zA-Z]+)$')
    return bool(pattern.match(string))
total_players = []
for i in ranks:
    if(i == 'MASTER' or i == 'GRANDMASTER' or i == 'CHALLENGER'):
        #as of now hold
        continue
    else:
        for k in tiers:
            players = get_players('na1',i,k,'RGAPI-337fe798-7e49-45ac-bc17-709096d45fab')
            total_players = total_players + players
random.shuffle(total_players)
with open('src/data/raw_data.txt','w') as f:
    for i in total_players:
        f.write(i)
        f.write('\n')
    print("Exported " + str(len(total_players)) + " players")
f.close()