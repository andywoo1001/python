import pandas as pd
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.dates import date2num


# from pandas import DataFrame

def Graph(code, start_date, end_date):

    DB = web.DataReader(code + str('.KS'), "yahoo", start_date, end_date)
    DB['MA20'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 20)
    DB['MA200'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 200)
    DB.to_csv(code + str('.csv'))

    DB = pd.read_csv(code + str('.csv'))

    DateIndex = []
    for index, row in DB.iterrows():
        DateIndex.append(date2num(datetime.strptime(row['Date'], "%Y-%m-%d")))
        #t = datetime.strptime(row['Date'], "%Y-%m-%d")
        #DateIndex.append( t.strftime("%Y%m%d") )


    # Display Chart
    scale = 1.5
    fig = plt.figure(figsize=(6 * scale, 4 * scale))
    # fig.set_size_inches(20,10)
    chart = plt.subplot(1, 1, 1)
    chart.plot_date(DateIndex, DB['Adj Close'], '-', color='#808080', linewidth=1.0, label='Close')
    chart.plot_date(DateIndex, DB['MA20'],      '-', color='#FF0000', linewidth=2.0, label='MA20')
    chart.plot_date(DateIndex, DB['MA200'],     '-', color='#0000FF', linewidth=2.0, label='MA200')
    chart.xaxis.set_major_locator(mticker.MaxNLocator(10))
    chart.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.axhline(y=0.0, xmin=0, xmax=1, hold=None)
    plt.title(code)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    #plt.subplots_adjust(left=0.05, bottom=0.05, right=0.96, top=0.96, wspace=0.2, hspace=0)

    plt.show()
    fig.savefig(code, dpi=600)


if __name__ == "__main__":
    code = '003490'  # 003490, 005930
    start_date = datetime(2011, 1, 1)
    end_date = datetime.now()

    Graph(code, start_date, end_date)