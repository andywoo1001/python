import pandas as pd
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import matplotlib
from matplotlib.finance import candlestick_ochl
matplotlib.rcParams.update({'font.size':9})

# from pandas import DataFrame

def Graph(code, start_date, end_date):

#    DB = web.DataReader(code + str('.KS'), "yahoo", start_date, end_date)
#    DB['MA20'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 20)
#    DB['MA200'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 200)
#    DB.to_csv(code + str('.csv'))

    DB = pd.read_csv(code + str('.csv'))

    CandleData = []
    DateIndex = []
    for index, row in DB.iterrows():
        date = datetime.strptime(row['Date'], "%Y-%m-%d")
        DateIndex.append(date2num(date))
        append_me = date2num(date), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']
        CandleData.append(append_me)


        #t = datetime.strptime(row['Date'], "%Y-%m-%d")
        #DateIndex.append( t.strftime("%Y%m%d") )


    # Display Chart
    scale = 1.0
    fig = plt.figure(figsize=(6 * scale, 4 * scale), facecolor='#07000d')

    #chart1 = plt.subplot(2, 1, 1)
    chart1 = plt.subplot2grid((5,4), (0,0), rowspan=4, colspan=4, axisbg='#07000d')
    chart1.plot_date(DateIndex, DB['Adj Close'], '-', color='#808080', linewidth=1.0, label='Close')
    chart1.plot_date(DateIndex, DB['MA20'],      '-', color='#FF0000', linewidth=2.0, label='MA20')
    chart1.plot_date(DateIndex, DB['MA200'],     '-', color='#0000FF', linewidth=2.0, label='MA200')
    #candlestick_ochl(chart1, CandleData, width=0.4, colorup='#77d879', colordown='#db3f3f')


    chart1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    chart1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    chart1.yaxis.label.set_color('#FFFFFF')
    chart1.spines['bottom'].set_color('#5998FF')
    chart1.spines['top'].set_color('#5998FF')
    chart1.spines['left'].set_color('#5998FF')
    chart1.spines['right'].set_color('#5998FF')
    #chart1.grid(False, color='#FFFFFF')

    plt.ylabel('Stock price')
    plt.axhline(y=0.0, xmin=0, xmax=1, hold=None)
    plt.title(code)
    plt.legend()
    plt.xticks(rotation=45)
    plt.setp(chart1.get_xticklabels(), visible=False)


    #chart2 = plt.subplot(2, 1, 2, sharex=chart1)
    chart2 = plt.subplot2grid((5,4), (4,0), sharex=chart1, rowspan=1, colspan=4, axisbg='#07000d')
    chart2.bar(DateIndex, DB['Volume'])
    #chart2.plot_date(DateIndex, DB['Volume'], '-', color='#808080', linewidth=1.0, label='Close')
    chart2.xaxis.set_major_locator(mticker.MaxNLocator(10))
    chart2.axes.yaxis.set_ticklabels([])
    chart2.grid(False)
    chart2.spines['bottom'].set_color('#5998FF')
    chart2.spines['top'].set_color('#5998FF')
    chart2.spines['left'].set_color('#5998FF')
    chart2.spines['right'].set_color('#5998FF')

    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.subplots_adjust(left=0.09, bottom=0.05, right=0.96, top=0.96, wspace=0.2, hspace=0)

    plt.show()
    fig.savefig(code, dpi=600)


if __name__ == "__main__":
    code = '003490'  # 003490, 005930
    start_date = datetime(2011, 1, 1)
    end_date = datetime.now()

    Graph(code, start_date, end_date)