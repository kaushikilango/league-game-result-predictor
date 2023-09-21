import requests as rq
import regex as re
API_KEY = 'RGAPI-550138ea-d9a7-4801-9be3-af687e027e16'
LEAGUES = ['challenger', 'grandmaster', 'master']

for k in LEAGUES:
    api_link = 'https://na1.api.riotgames.com/lol/league/v4/' + k + 'leagues/by-queue/RANKED_SOLO_5x5?api_key=' + API_KEY

    response = rq.get(api_link)
    data = response.json()

    d = []
    for i in data['entries']:
        d.append(i['summonerName'])
    pattern = re.compile('^[a-zA-Z0-9 ]*$')
    dt = []
    print(d[:30])
    for i in d[:30]:
        if pattern.match(i):
            s = '(' + i + ',' + k.upper() + ')'
            dt.append(s)
    print(dt)
    with open('data\leader_data.txt','a') as f:
        for lines in dt:
            f.write(f"{lines}\n")
    print('Done for: ',k)      
