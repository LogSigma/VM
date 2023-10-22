# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 08:47:14 2023

@author: logsigma
"""

import pandas as pd
from itertools import product

print('파일(csv)이름을 입력하세요. :', end='')
file_name = input()
print('Y값 컬럼을 입력하세요. :', end='')
target = input()
print('조합(Combination) 할 개수를 입력하세요. :', end='')
comb = int(input())

df = pd.read_csv(file_name)
fetures = [col for col in df.columns if col != target]

avg = df[fetures].mean()
plus = ['+','-','/','*']


def funPlus(dfa, dfb, p):
    if p == '+':
        return pd.DataFrame(dfa + dfb)
    elif p == '-':
        return pd.DataFrame(dfa - dfb)
    elif p == '*':
        return pd.DataFrame(dfa * dfb)
    else:
        return pd.DataFrame(dfa / dfb)

def tstar(data, n):
    fet = [col for col in data.columns if col != target]
    fetures_c = list(product(fet,fetures))
    for i1, i2 in fetures_c:
        if i1 == i2:
            pass
        else:
            for p in plus:
                # print(i1,i2,p)
                #data = pd.concat([data, funPlus(data[f'{i1}'], data[f'{i2}'], p)], axis=1)
                name = '(' + f'{i1}{p}{i2}'+ ')'
                if name not in fet:
                    data.loc[:, name] = funPlus(data[f'{i1}'], data[f'{i2}'], p)
    if n == 2:
        pass
    else:
        tstar(data, n - 1)


def tavg(data):
    fet = [col for col in data.columns if col != target]
    for fe in fet:
        for i in range(len(fetures)):
            if fe == fetures[i]:
                pass
            else:
                name = f'{fe}/{fetures[i]}_AVG'
                data.loc[:, name] = funPlus(data[f'{fe}'], avg[i], '/')
        

tstar(df,comb)
tavg(df)

result = df.corr(method='pearson')[target].sort_values(ascending=False).iloc[1:]
result = result.reset_index()

#result.head(10)
result.to_csv(f'{file_name}_result.csv', index=False)
