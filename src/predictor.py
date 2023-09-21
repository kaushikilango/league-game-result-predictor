import pandas as pd
import numpy as np
import scipy.stats as stats

DATA_COLUMNS = ['ally_tower_kills','enemy_tower_kills','ally_inhibitor_kills','enemy_inhibitor_kills','ally_baron_kills','enemy_baron_kills','ally_dragon_kills','enemy_dragon_kills',
                'ally_rift_kills','enemy_rift_kills','ally_kills','enemy_kills','score_diff','win','rank']

def get_data():
    df = pd.read_csv('data\master_data.csv')
    return df

def randomizer(df):
    df = df.sample(frac=1)
    df.reset_index(drop=True, inplace=True)
    return df

def get_percentage(df,rank):
    f = len(df[(df['rank'] == rank)]) / len(df) * 100
    return f

if __name__ == '__main__':
    d = get_data()
    d.columns = DATA_COLUMNS
    d = randomizer(d)
    print(d.head())

    for i in ['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']:
        print('The percentage of ',i.lower(),' players in the dataset is: ',get_percentage(d,i),'%')
