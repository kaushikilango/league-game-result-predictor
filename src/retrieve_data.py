import requests as rq
from tqdm import tqdm
import pandas as pd
from score_calculator import calculate_game_scores
from team_dets import scrutinize_team
import time
from data_ret import get_account_info,get_match_list,get_match_details,get_participants_details
import ast
api_key = 'RGAPI-337fe798-7e49-45ac-bc17-709096d45fab'
server = 'na1'
shard = 'americas'
summoner_name = 'Savage Buffalo1'
max_requests = 10 # per time_frequency
time_frequency = 1 # in seconds
queue_id = 420  # ranked solo/duo ## 400 is normal draft #430 is blind pick

player_pair = []
with open('src/data/raw_data.txt','r') as f:
    player1 = f.readlines()
    for i in player1:
        i = i.replace('(' ,'')
        i = i.replace(')' ,'')
        x = tuple(i.split(','))
        player_pair.append(x)
print('Starting Analysis at ',time.strftime("%H:%M:%S", time.localtime()))
print('Total players to be analyzed: ',len(player_pair))
for i,k in player_pair:
    k = k.replace('\n','')
    print('Running Analysis for Player: ',i,' in elo: ',k)
    summoner_name = i
    e = k
    puuid = get_account_info(summoner_name, server, api_key)[1]  ## this will get the puuid of the summoner
    matches = []
    for i in range(0,1):
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
    elo = [e] * df.shape[0]
    df['elo'] = elo
    print('Process ended at ',time.strftime("%H:%M:%S", time.localtime()))
    df.to_csv('src/data/' + summoner_name.replace(' ','_') + '.csv')  ## This will save the dataframe as a csv file'''
    df.to_csv('src/data/master_data.csv',mode='a',index=False,header=False)
    time.sleep(60)



