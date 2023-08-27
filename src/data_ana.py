import pandas as pd

df =  pd.read_csv('data.csv')
print(df.head())
df['killParticipation'] = df['killParticipation'].fillna(df['killParticipation'].mean())
print(df['killParticipation'].mean() * 100)
print(sum((df['win']) & (df['lane'] == 'JUNGLE')) / sum(df['lane'] == 'JUNGLE') * 100)
