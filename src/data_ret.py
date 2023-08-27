import requests as rq
from tqdm import tqdm
import pandas as pd

api_key = 'RGAPI-93292044-0328-4ca9-ba0e-e71230b871d1'
server = 'na1'
shard = 'americas'
summoner_name = 'miman'
max_requests = 10 # per time_frequency
time_frequency = 1 # in seconds
queue_id = 420  # ranked solo/duo ## 400 is normal draft #430 is blind pick

def get_account_info(summoner_name, server, api_key):
    account_link = 'https://' + server + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + api_key
    account_info = rq.get(account_link).json()
    account_id = account_info['accountId']
    puuid = account_info['puuid']
    return account_id, puuid

def get_match_list(puuid, shard, api_key):
    match_list_link = 'https://' + shard + '.api.riotgames.com/lol/match/v5/matches/by-puuid/'+ puuid + '/ids' +'?type=ranked' + '&api_key=' + api_key + '&count=100' + '&queue=' + str(queue_id)
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
    return player_stats

puuid = get_account_info(summoner_name, server, api_key)[1]
matches = get_match_list(puuid, shard, api_key)
keys = ['assists','championId','champExperience','deaths','firstTowerKill','inhibitorKills','kills','lane',
        'longestTimeSpentLiving','turretsLost','turretKills','win']
challenges = ['acesBefore15Minutes', 'bountyGold', 'damagePerMinute', 'firstTurretKilled', 'gameLength', 'kda', 'killParticipation','maxCsAdvantageOnLaneOpponent', 'maxKillDeficit', 'multikills', 'soloKills', 'takedowns', 'teamBaronKills','turretPlatesTaken','turretTakedowns']
data = []
for match in tqdm(matches):
    match_detail = get_match_details(match, shard, api_key)
    participant_details = get_participants_details(match_detail, get_account_info(summoner_name, server, api_key)[1])
   # print(participant_details)
    pd_df = {key: participant_details[key] for key in keys}
    pd_challenges = {key: (participant_details['challenges'][key] if key in participant_details['challenges'] else None) for key in challenges}
    pd_df.update(pd_challenges)
    sorted_keys = list(pd_df.keys())
    sorted_keys.sort()
    pd_df = {key: pd_df[key] for key in sorted_keys}
    data.append(pd_df)
df = pd.DataFrame(data, columns = (keys + challenges).sort())
## Lets try to insert data into a dataframe by using the above api calls
## We will use the pandas library to create a dataframe
print(df.shape)        ## This will print the shape of the dataframe
df.to_csv('data.csv')  ## This will save the dataframe as a csv file