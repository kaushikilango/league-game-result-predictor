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

def categorize_rank(df):
    rank_to_num = {'CHALLENGER': 9, 'GRANDMASTER': 8, 'MASTER': 7, 'DIAMOND': 6, 'PLATINUM': 5, 'GOLD': 4, 'SILVER': 3, 'BRONZE': 2, 'IRON': 1}
    df['rank'] = df['rank'].map(rank_to_num)
    return df
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
    X = d.drop(['_id','win'],axis=1)
    rank_onehot = pd.get_dummies(X['rank']).astype(int)
    X = pd.concat([X,rank_onehot],axis=1)
    X.drop(['rank'],axis=1,inplace=True)
    y = d['win']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    print('The current shape of the feature training set is: ',X_train.shape)
    print('The current shape of the feature test set is: ',X_test.shape)
    print('The current shape of the label training set is: ',y_train.shape)
    print('The current shape of the label test set is: ',y_test.shape)
    from sklearn.preprocessing import StandardScaler
    print(X_train.head())
    scaler = StandardScaler()

    from sklearn.linear_model import LogisticRegression
    regressor = LogisticRegression()
    regressor.fit(X_train,y_train)
    y_pred = regressor.predict(X_test)
    print(y_pred)
    print(y_test)
    from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
    acc = accuracy_score(y_test,y_pred)
    cls_report = classification_report(y_test,y_pred)
    con_mat = confusion_matrix(y_test,y_pred)
    print('The accuracy of the model is: ',acc)
    print('The classification report of the model is: ',cls_report)
    print('The confusion matrix of the model is: ',con_mat)

    