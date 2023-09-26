import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.model_selection import train_test_split


def get_data():
    df = pd.read_csv("C:\Git\league-game-result-predictor\src\data\master_data.csv")
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
    d = randomizer(d)
    print(d.head())
    print('The current shape of the dataset is: ',d.shape)
    for i in ['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']:
        print('The percentage of ',i.lower(),' players in the dataset is: ',get_percentage(d,i),'%')
    print('Checking for duplicates in the dataset...')
    print(f'There are {d.duplicated().sum()} duplicates in the dataset')
    print('Removing duplicates...')
    d.drop_duplicates(inplace=True)
    print('Checking for duplicates in the dataset...')
    print(f'There are {d.duplicated().sum()} duplicates in the dataset')
    print('The current shape of the dataset is: ',d.shape)
    print('Checking for null values in the dataset...')
    print(f'There are {d.isnull().sum().sum()} null values in the dataset')
    print('Removing null values...')
    d.dropna(inplace=True)
    print('Checking for null values in the dataset...')
    print(f'There are {d.isnull().sum().sum()} null values in the dataset')
    print('The current shape of the dataset is: ',d.shape)
    print('Checking for outliers in the dataset...')
    X = d.drop('win',axis=1)
    y = d['win']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    print('The current shape of the feature training set is: ',X_train.shape)
    print('The current shape of the feature test set is: ',X_test.shape)
    print('The current shape of the label training set is: ',y_train.shape)
    print('The current shape of the label test set is: ',y_test.shape)
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import OneHotEncoder
    encoder = OneHotEncoder()
    scaler = StandardScaler()
    encoder.fit(X_train[['rank']])
    