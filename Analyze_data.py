import pandas as pd

#creating panda dataframe

data_df = pd.read_csv('new_cases.csv')
data_df2= pd.read_csv('DATAFRAME.csv')

# df["Unique"] = data_df.columns.isin(data_df2["location"])

# print (data_df.columns)
# print (data_df2["location"])

countires=data_df.columns[data_df.columns.isin(data_df2["location"])].tolist()
countires.append('date')
data_df3=data_df[countires]

# data_df2[data_df['location'] == 'India'].shape[0]

# count_fakes=data_df2[data_df2['location'] == 'India'].groupby(['date']).count().drop(['location', 'verifier'], axis = 1)
# # count_fakes.index.tolist()

# count_fakes.index=pd.to_datetime(count_fakes.index).date
# data_df3['date']=pd.to_datetime(data_df3['date'])
# data_df3=data_df3[['date','India']][data_df3['date'].isin(count_fakes.index.tolist())]
# count_fakes = count_fakes.loc[:, ~count_fakes.columns.str.contains('^Unnamed')]
# count_fakes.index=count_fakes.index.rename('date')
# data_df3=data_df3.set_index('date')

# result = pd.concat([data_df3, count_fakes], axis=1,  join='inner')


count_fakes=data_df2[data_df2['location'] == 'India'].groupby(['date']).count().drop(['location', 'verifier'], axis = 1)

count_fakes.index=pd.to_datetime(count_fakes.index).date
data_df3['date']=pd.to_datetime(data_df3['date'])
data_df3=data_df3[['date','India']][data_df3['date'].isin(count_fakes.index.tolist())]
count_fakes = count_fakes.loc[:, ~count_fakes.columns.str.contains('^Unnamed')]
count_fakes.index=count_fakes.index.rename('date')
data_df3=data_df3.set_index('date')

result = pd.concat([data_df3, count_fakes], axis=1,  join='inner')
result['fakenews'] = result['fakenews']*-1
print(result)


