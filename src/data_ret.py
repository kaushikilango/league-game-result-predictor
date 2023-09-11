import requests as rq
from tqdm import tqdm
import pandas as pd
from score_calculator import calculate_game_scores
api_key = 'RGAPI-5b57ebaf-54c6-4816-8c2c-7cf91eb6f345'
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

def get_match_list(puuid, shard, api_key,queue_id=queue_id,count = 100):
    match_list_link = 'https://' + shard + '.api.riotgames.com/lol/match/v5/matches/by-puuid/'+ puuid + '/ids' + '?api_key=' + api_key + '&count='+str(count) + '&queue=' + str(queue_id)
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
matches = get_match_list(puuid, shard, api_key)   ## this will get the match list of the summoner based on the conditions we already fixed in the function
print(matches)

''' I think we could implement this in the function and could make it more efficient but for now we will just use this as it is'''
if len(matches) < 100:  ## if the number of matches is less than 100 then we will get the match list again but this time we will use the normal draft games as difference
    print('Not enough matches to analyze')
    print('Executing retrieval of match list again but using the normal draft games as difference')
    matches = matches + get_match_list(puuid, shard, api_key, queue_id=400,count = 100 - len(matches))
    if len(matches) < 100:
        print('Not enough matches to analyze')
    print('Executing retrieval of match list again but using the normal blind games as difference')
    matches = matches + get_match_list(puuid, shard, api_key, queue_id=430,count = 100 - len(matches))   
keys = ['assists','championId','champExperience','deaths','firstTowerKill','inhibitorKills','kills','lane',
        'longestTimeSpentLiving','turretsLost','turretKills','win']
challenges = ['acesBefore15Minutes', 'bountyGold','baronTakedowns', 'damagePerMinute','doubleAces','earlyLaningPhaseGoldExpAdvantage ', 'firstTurretKilled', 'gameLength', 'kda', 'killParticipation','maxCsAdvantageOnLaneOpponent','landSkillShotsEarlyGame ', 'maxKillDeficit','maxLevelLeadLaneOpponent', 'multikills', 'soloKills', 'takedowns', 'teamBaronKills','turretPlatesTaken','turretTakedowns']
data = []
for match in tqdm(matches):
    match_detail = get_match_details(match, shard, api_key)
    participant_details,plyr_index = get_participants_details(match_detail, get_account_info(summoner_name, server, api_key)[1])
   # print(participant_details)
    scores = calculate_game_scores(match_detail['info']['participants'],match)
    plyr_score = scores[plyr_index]
    pd_df = {key: participant_details[key] for key in keys}
    print(participant_details)
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