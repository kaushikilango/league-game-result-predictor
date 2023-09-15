import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('src\data\lane_data.csv')
df = df.drop(['Unnamed: 0'],axis=1)
win_percentage = df['win'].sum()/df.shape[0]
outlier_loss = df[(df['score_diff'] < 0) & (df['win'] == True)]
outlier_win = df[(df['score_diff'] > 0) & (df['win'] == False)]
print(len(outlier_loss))
print(len(outlier_win))
print(win_percentage*100)
plt.plot(df['score_diff'],df['win'],'ro')
plt.show()