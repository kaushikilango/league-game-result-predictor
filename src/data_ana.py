import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('data.csv')
df = df.drop(['Unnamed: 0'],axis=1)
df['score'] = df['score'].apply(lambda x: x*10)

plt.plot(df['score_diff'],df['win'],'ro')
plt.show()