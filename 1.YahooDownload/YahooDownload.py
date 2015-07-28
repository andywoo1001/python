# !/usr/bing/python

import pandas.io.data as web
import pandas as pd
import datetime
import matplotlib.pyplot as plt

start = datetime.datetime(2000, 1, 1)
end = datetime.datetime.today()


def output_cvs(name):
    DB = web.DataReader(name + str('.KS'), "yahoo", start, end)
    DB['MA30'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 30)
    DB['MA60'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 60)
    DB['MA120'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 120)
    DB['MA240'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 240)
    DB.to_csv(name + str('.csv'))
    plt.plot(DB.index, DB['Adj Close'], 'r')
    plt.plot(DB.index, DB['MA240'], 'b')
    plt.show()


f = open('KOSPI.txt')
lists = f.readlines()

for item in lists:
    name = item.split('\n')[0]
    output_cvs(name)
