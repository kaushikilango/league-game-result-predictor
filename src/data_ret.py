import requests as rq
from tqdm import tqdm
import pandas as pd
from score_calculator import calculate_game_scores
from team_dets import scrutinize_team
import time
api_key = 'RGAPI-5792b231-e1db-40f7-9e6a-d6f7ddfbb67c'
server = 'na1'
shard = 'americas'
summoner_name = 'Miraa'
max_requests = 10 # per time_frequency
time_frequency = 1 # in seconds
queue_id = 420  # ranked solo/duo ## 400 is normal draft #430 is blind pick
challenger = ['Cody Sun','Amazo','Fishlord','Yuxin Baby','TWTV Daption']
grandm = {'player': ['Big Dacko','AXSOLUTE','OnlyOnesWhoKnow','Shockey','Young7'], 'elo' : 'grandmaster'}
master = {'players': ['GreasyBigMac','Alson','Miraa','Greed','HunterxNh'], 'elo': 'master'}
emerald = {'players': ['Octonaut','Forced Consent','poph55','enarwis','JAJA A'], 'elo': 'emerald'}
platinum = {'players': ['Hahn','Egyptian Pyke','Yuumi Boom','KumakoDX','iki11noob'], 'elo': 'platinum'}
gold = {'players': ['Rhinocesaurus','NAYoungBeuwolf','SuperNinja333','no peroxide','bronze v rules'], 'elo': 'gold'}
def get_account_info(summoner_name, server, api_key):
    account_link = 'https://' + server + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + api_key
    account_info = rq.get(account_link).json()
    account_id = account_info['accountId']
    puuid = account_info['puuid']
    return account_id, puuid

def get_match_list(puuid, shard, api_key,queue_id=queue_id,count = 100,start = 0):
    match_list_link = 'https://' + shard + '.api.riotgames.com/lol/match/v5/matches/by-puuid/'+ puuid + '/ids' + '?api_key=' + api_key + '&count='+str(count) + '&start=' + str(start)
    match_list = rq.get(match_list_link).json()
    return match_list

def get_match_details(match_id, shard, api_key):
    match_details_link = 'https://' + shard + '.api.riotgames.com/lol/match/v5/matches/' + match_id + '?api_key=' + api_key
    match_details = rq.get(match_details_link).json()
    return match_details

def get_participants_details(match_details, puuid):
    player_chr = match_details['metadata']['participants'].index(puuid)  ## finding the chronical number of the player

    player_stats = match_details['info']['participants'][player_chr]

    player_team = player_stats['teamId']
    team_win = player_stats['win']
    return player_stats,player_chr

puuid = get_account_info(summoner_name, server, api_key)[1]  ## this will get the puuid of the summoner
matches = []
for i in range(0,601,100):
    matches = matches + get_match_list(puuid, shard, api_key)   ## this will get the match list of the summoner based on the conditions we already fixed in the function
print(matches)
keys = ['assists','championId','champExperience','deaths','firstTowerKill','inhibitorKills','kills','lane',
        'longestTimeSpentLiving','turretsLost','turretKills','win','score','score_diff']
team_dt = ['ally_tower_kills','enemy_tower_kills','ally_inhibitor_kills','enemy_inhibitor_kills',
        'ally_baron_kills','enemy_baron_kills','ally_dragon_kills','enemy_dragon_kills',
        'ally_rift_kills','enemy_rift_kills','ally_kills','enemy_kills']
data = []
count = 0
total_matches = 0
for match in tqdm(matches):
    match_detail = get_match_details(match, shard, api_key)
    count = count + 1
    if count%80 == 0:
        time.sleep(120)
    if match_detail['info']['gameDuration'] > 1380:
        total_matches = total_matches + 1
        participant_details,plyr_index = get_participants_details(match_detail, get_account_info(summoner_name, server, api_key)[1])
        scores,score_diff = calculate_game_scores(match_detail['info']['participants'],match)
        team_data = scrutinize_team(match_detail['info']['teams'],participant_details['teamId'])
        plyr_score,player_score_diff = scores[plyr_index],score_diff[plyr_index]
        participant_details['score'] = plyr_score
        participant_details['score_diff'] = player_score_diff
        pd_df = {key: participant_details[key] for key in keys}
        pd_df.update(team_data)
        sorted_keys = list(pd_df.keys())
        sorted_keys.sort()
        pd_df = {key: pd_df[key] for key in sorted_keys}
        data.append(pd_df)
print('Total matches retrieved: ',count)
print('Total matches analyzed: ',total_matches)
df = pd.DataFrame(data, columns = (keys + team_dt).sort())
df = df[team_dt + ['score_diff','win']]
print(df.head())
## Lets try to insert data into a dataframe by using the above api calls
## We will use the pandas library to create a dataframe
print(df.shape)        ## This will print the shape of the dataframe
df.to_csv('src/data/Miraa_data.csv')  ## This will save the dataframe as a csv file