import pandas as pd
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num
import os

# from pandas import DataFrame



if __name__ == "__main__":
	
	StartDate 	= datetime(2011,1,1)
	EndDate 	= datetime(2015,6,30)

	DB = []
	#path = '../../historical.data/yahoo.csv/'
	path = './'
	for file in os.listdir(path):
		if file.endswith(".csv"):
			table = pd.read_csv(path+file)
			DB.append(table)

	print (len(DB))
	for idx in len(DB)
		DB[0]


