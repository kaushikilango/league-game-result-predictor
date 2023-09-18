import pandas as pd


player_pair = []
with open('src/data/raw_data.txt','r') as f:
    player1 = f.readlines()
    for i in player1:
        x =  tuple(i.replace('\n','').split(','))
        print(x)
        player_pair.append(x)
print(player_pair)

for i,k in player_pair:
    summoner_name = i
    print("Running for: ",summoner_name)
    d = pd.read_csv('src/data/' + summoner_name.replace(' ','_') + '.csv')
    df = d.drop(['Unnamed: 0'],axis=1)
    master = pd.read_csv('src/data/match_data.csv')
    master = pd.concat([master,df],axis = 0)
    master.to_csv('src/data/match_data.csv')
    print('Done for: ',summoner_name)


