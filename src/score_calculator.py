## Calculating the score of a player in a game

import pandas as pd
import numpy
import copy
def calculate_game_scores(game1,game_id):
    game = copy.deepcopy(game1)
    for k in game:
        del k['perks']
        c = k['challenges']
        k.update(c)
        del k['challenges']
        k.update({'_MATCHID': 'NA1_4762661935'})
    df = pd.DataFrame(game)
    dmgteam1 = df[df['teamId']==100]['totalDamageDealtToChampions'].sum()
    dmgteam2 = df[df['teamId']==200]['totalDamageDealtToChampions'].sum()
    df["percentageDamage"] = df.apply(lambda x: x['totalDamageDealtToChampions']/dmgteam1 if x['teamId']==100 else x['totalDamageDealtToChampions']/dmgteam2, axis=1)
    df['damagePerDeath'] = df['totalDamageDealtToChampions']/df['deaths']
    df['csPerMin'] = df['totalMinionsKilled']/df['gameLength']*60
    df['score'] = df['kda'].apply(lambda x: min(x/2.51,1)* 0.27) + df['killParticipation'].apply(lambda x: min(x/0.471,1) * 0.13) + df['damagePerDeath'].apply(lambda x: min(x/3770,1)*0.15) + df['percentageDamage'].apply(lambda x: min(x/0.228,1)*0.15) + df['csPerMin'].apply(lambda x: min(x/6.8,1)*0.10) + df['goldPerMinute'].apply(lambda x: min(x/369.1,1)*0.10) + df['visionScorePerMinute'].apply(lambda x: min(x/0.3,1)*0.10)
    df['score'] = df['score']* 10
    print(df['score'])
    return numpy.array(df['score'])
## Calculating cumulative properties
