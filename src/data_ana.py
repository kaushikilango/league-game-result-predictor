import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('data.csv')
df = df.drop(['Unnamed: 0'],axis=1)
win_percentage = df['win'].sum()/df.shape[0]

print(win_percentage*100)
plt.plot(df['score_diff'],df['win'],'ro')
plt.show()