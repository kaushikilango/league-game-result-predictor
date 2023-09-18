import requests as rq
import time
print('Process started at ',time.strftime("%H:%M:%S", time.localtime()))
def get_account_info(summoner_name, server, api_key):
    account_link = 'https://' + server + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + api_key
    account_info = rq.get(account_link).json()
    account_id = account_info['accountId']
    puuid = account_info['puuid']
    return account_id, puuid

def get_match_list(puuid, shard, api_key,queue_id=420,count = 50,start = 0):
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
