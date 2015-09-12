# -*- coding: utf-8 -*-

import pandas as pd
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num


# from pandas import DataFrame

def Download_Lastest_Data(name, start, Baseline, Crossline):
	end = datetime.now()
	DB = web.DataReader(name + str('.KS'), "yahoo", start, end)
	if (Baseline != 'Adj Close'):
		DB[Baseline] = pd.stats.moments.rolling_mean(DB['Adj Close'], int(Baseline[2:]) )
	DB[Crossline] = pd.stats.moments.rolling_mean(DB['Adj Close'], int(Crossline[2:]) )
	DB['DIFF'] = (DB[Baseline] - DB[Crossline])  # 'Adj Close' 'MA30'
	# plt.plot(DB.index, DB['Adj Close'], 'r')
	# plt.plot(DB.index, DB['MA240'], 'b')
	# plt.plot(DB.index, DB['D240'], 'g')
	# plt.axhline(y=0.0, xmin=0, xmax=1, hold=None)
	# plt.show()
	DB.to_csv(name + str('.csv'))


def Read_CVS_Files(name, Baseline, Crossline):
	DB = pd.read_csv(name)

	oldValue = 0.0
	Initial_Account_Value = 10000000.0  #
	Total_Value = Initial_Account_Value
	Quantity = 0  # number of stock purchased
	Change = 0.0
	BUY = 0.0
	SELL = 0.0
	BUY_Date = ""
	SELL_Date = ""
	BUY_Index = 0
	SELL_Index = 0
	isOpenPosition = False
	Trade_Index = 0
	ohlc = []
	DateIndex = []
	for index, row in DB.iterrows():
		Date = row['Date']
		Price = row[Baseline]  # 'Adj Close' 'MA30'
		MA240 = row[Crossline]
		Value = row['DIFF']
		if (oldValue < 0.0 and Value >= 0.0):  # BUY ( minus(-) to plus(+) )
			isOpenPosition = True
			BUY = Price
			BUY_Date = Date
			BUY_Index = index
			Quantity = int(Total_Value / Price)
		# print("%4d, Date:%s Price:%8.2f, MA240:%8.2f, %8.2f %8.2f BUY@ %8.2f" % (index, Date, Price, MA240,  oldValue, Value, Price))
		elif (oldValue >= 0.0 and Value < 0.0 and isOpenPosition == True):
			SELL = Price
			SELL_Date = Date
			SELL_Index = index
			GainLoss = (SELL - BUY) * float(Quantity)
			Change = ((SELL - BUY) / BUY) * 100.0
			Total_Value += GainLoss
			Trade_Index += 1
			Hold_Period = (SELL_Index - BUY_Index)
			isOpenPosition = False
			print("[%2d] Total Value: %15.2f,  Gain/Loss:%12.2f   Qty:%4d  Chg:%7.2f%%  Hold Period:%4d (BUY %s @%9.2f => SELL %s @%9.2f)" % (
				Trade_Index, Total_Value, GainLoss, Quantity, Change, Hold_Period, BUY_Date, BUY, SELL_Date, SELL))
		# print("%4d, Date:%s Price:%8.2f, MA240:%8.2f, %8.2f %8.2f             SELL@ %8.2f" % (index, Date, Price, MA240,  oldValue, Value, Price))
		# else:
		# print("%4d, Date:%s Price:%8.2f, MA240:%8.2f, %8.2f %8.2f" % (index, Date, Price, MA240,  oldValue, Value))
		oldValue = Value
		#append_me = date2num(datetime.strptime(Date,"%Y-%m-%d")), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']
		#ohlc.append(append_me)
		DateIndex.append(date2num(datetime.strptime(row['Date'],"%Y-%m-%d")))

	# Calculate any open position into Account
	if (isOpenPosition == True):
		SELL = Price
		SELL_Date = Date
		SELL_Index = index
		GainLoss = (SELL - BUY) * float(Quantity)
		Change = ((SELL - BUY) / BUY) * 100.0
		Total_Value += GainLoss
		Trade_Index += 1
		Hold_Period = (SELL_Index - BUY_Index)
		print("[%2d] Total Value: %15.2f,  Gain/Loss:%12.2f   Qty:%4d  Chg:%7.2f%%  Hold Period:%4d (BUY %s @%9.2f => SELL %s @%9.2f)" % (
			Trade_Index, Total_Value, GainLoss, Quantity, Change, Hold_Period, BUY_Date, BUY, SELL_Date, SELL))

	Investment = '{:,.0f}'.format(Initial_Account_Value)
	Current_Value = '{:,.0f}'.format(Total_Value)
	Net_Profit = '{:,.0f}'.format(Total_Value - Initial_Account_Value)
	print("SUMMARY: Investment= ₩/%s, Current Value= ₩%s  Net Profit= ₩%s  ROI= %.2f" % (
	Investment, Current_Value, Net_Profit, (Total_Value / Initial_Account_Value)))

	#DB['DateIdx'] = datetime.strptime(DB['Date'],"%Y-%m-%d")

	# Display Chart
	scale = 1.5
	fig = plt.figure(figsize=(6 * scale, 4 * scale))
	# fig.set_size_inches(20,10)
	chart = plt.subplot(1, 1, 1)
	# chart.plot_date(DB['Date'], DB[Baseline], 'r', label='Close') #'Adj Close' 'MA30
	chart.plot_date(DateIndex, DB[Baseline], 'r', label=Baseline)  # 'Adj Close' 'MA30
	chart.plot_date(DateIndex, DB[Crossline], 'b', label=Crossline)
	chart.plot_date(DateIndex, DB['DIFF'], 'g', label='Difference')
	#candlestick_ohlc(chart, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')

	plt.axhline(y=0.0, xmin=0, xmax=1, hold=None)
	plt.title(name[:-4]+" "+Crossline+'-based trading back test')
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.legend()
	plt.grid(True)
	#plt.xticks(rotation=70)
	plt.subplots_adjust(left=0.05, bottom=0.05, right=0.96, top=0.96, wspace=0.2, hspace=0)

	plt.show()
	fig.savefig('capture.png', dpi=600)


if __name__ == "__main__":
	KOSPI 		= '003490'  # 003490, 005930
	Baseline 	= 'Adj Close'  # 'Adj Close', 'MA5', 'MA10', 'MA30', 'MA60'
	Crossline 	= 'MA240'
	Start_Date 	= datetime(2011,1,1)

	Download_Lastest_Data(KOSPI, Start_Date, Baseline, Crossline)
	Read_CVS_Files(KOSPI+'.csv', Baseline, Crossline)
