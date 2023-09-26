import string
import random
import pandas as pd
def random_id():
    s = list(string.ascii_letters)
    f = list(range(10))
    j = f + s
    r = []
    r.append('NA')
    for x in range(20):
        r.append(str(random.choice(j)))
    return ''.join(r)

DATA_COLUMNS = ['ally_tower_kills','enemy_tower_kills','ally_inhibitor_kills','enemy_inhibitor_kills','ally_baron_kills','enemy_baron_kills','ally_dragon_kills','enemy_dragon_kills',
                'ally_rift_kills','enemy_rift_kills','ally_kills','enemy_kills','score_diff','win','rank']

df = pd.read_csv("C:/Users/kilan/OneDrive/Desktop/master_data.csv")

df.columns = DATA_COLUMNS

df['_id'] = df.apply(lambda x: random_id(), axis=1)
df = df.sort_values(by=['_id'])
df = df.sort_index(axis=1)
df.to_csv("C:/Users/kilan/OneDrive/Desktop/master_data.csv", index=False)