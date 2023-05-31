# -*- coding: utf-8 -*-
"""
Created on Wed May 31 19:10:24 2023

@author: logsigma
"""

import pandas as pd
import matplotlib.pyplot as plt
 
k = 10
count = 5

df = pd.read_excel('D:/python/data.xlsx')

df.head()

df['LOTID_ID'] = df[['LOTID','NO']].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)


df['EQPID_CAMID'] = df[['EQPID','CAMID']].apply('_'.join, axis=1)
df['STD']= 0

dfs = df.dropna(subset=['Y']).reset_index()

for i in range(len(dfs)-k):
    tmp_dfs = dfs[i:i+k]
    
    tmp_dfs['Y_S'] = abs((tmp_dfs['Y']- tmp_dfs['Y'].mean())/tmp_dfs['Y'].std())
    tmp_dfs['Y_PID_S'] = abs((tmp_dfs['Y_PID']- tmp_dfs['Y_PID'].mean())/tmp_dfs['Y_PID'].std())
    tmp_dfs = tmp_dfs.sort_values('Y_S')
    tmp_dfs = tmp_dfs[:count]
    stds = tmp_dfs['Y'].mean() - tmp_dfs['Y_PID'].mean()
    dfs.loc[i+k, 'STD'] = stds

dfss = dfs[['LOTID_ID','STD']]

df = pd.merge(df, dfss, how='left', on = "LOTID_ID")

df['STD_y'] = df['STD_y'].fillna(method='ffill')

df['Y_PID'+str(k)] = df['Y_PID'] + df['STD_y']
dfs['Y_PID'+str(k)] = dfs['Y_PID'] + dfs['STD']

fig, ax = plt.subplots(1, 1)
plt.plot(df['NO'], df['Y'], label='Y', marker='.')
plt.plot(df['NO'], df['Y_PID'], label='Y_PRID', marker='.')
plt.plot(df['NO'], df['Y_PID'+str(k)], label='Y_STD', marker='.')
plt.grid()
plt.legend()
plt.yticks(fontsize=13)
plt.show()

fig, ax = plt.subplots(1, 1)
plt.plot(dfs['NO'], dfs['Y'], label='Y', marker='.', color='#0000FF')
plt.plot(dfs['NO'], dfs['Y_PID'], label='Y_PRID', marker='.')
plt.plot(dfs['NO'], dfs['Y_PID'+str(k)], label='Y_STD', marker='.', color='#FF0000')
plt.legend()
plt.yticks(fontsize=13)
plt.show()
plt.show()
