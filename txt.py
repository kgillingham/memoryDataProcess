import sys
import pandas as pd


data = pd.read_csv(sys.argv[1], sep=',')
data['Timestamp'].replace(to_replace=r'[^0-9\.]', value='', inplace=True, regex=True)
data['Timestamp'].replace(to_replace=r'^0(?=\d+)', value='', inplace=True, regex=True)
data['Timestamp'] = data['Timestamp'].astype('float').round(3)
data['Absolute(ns)'] = data['Timestamp'].cumsum().astype('int64')

data['data0'].to_string()
data['data0'].replace(to_replace=r'[^\w]', value='', inplace=True, regex=True)
data['data0'].replace(to_replace=r'^\w', value='', inplace=True, regex=True)
data['CLE'] = data['data0'].where(data['CLE_0'] == 1).astype('string')
data['ALE'] = data['data0'].where(data['ALE_0'] == 1).astype('string')

data.to_csv('yob.csv')