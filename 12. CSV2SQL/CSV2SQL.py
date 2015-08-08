import pandas as pd
import os
import time
from datetime import datetime
from matplotlib.dates import date2num
import sqlite3

# Create NEW SQL database
connect = sqlite3.connect('Yahoo_sqlite.db')
cursor = connect.cursor()


PATH = '/Users/insuyu/GitHub/historical.data/yahoo.csv/'
#PATH = '/Users/insuyu/GitHub/python/12. CSV2SQL/'


# Create a New Table for Code
# DateStamp(REAL) | Date(TEXT) | Open(REAL) | High(REAL) | Low(REAL) 
#    | Close(REAL) | Volume(REAL) | AdjClose(REAL) | MA20(REAL) | MA30(REAL) | MA200(REAL) | MA240 (REAL)
command = "CREATE TABLE YAHOO(Code TEXT, DateStamp INT, Date TEXT, Open REAL, High REAL, Low REAL, Close REAL, Volume INT, AdjClose REAL, MA20 REAL, MA30 REAL, MA200 REAL, MA240 REAL)"
print(command)
cursor.execute(command)

# For All Files in PATH
nFiles = 0
for filename in os.listdir(PATH):
    # Find only *.csv files
    if filename.endswith(".csv"):
        print ("[%d] %s" % (nFiles, filename))
        # Load CVS to Database
        DB = pd.read_csv(PATH+filename)
    
        # Generate Moving Average Data
        DB['MA20'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 20)
        DB['MA30'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 30)
        #DB['MA30'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 30)
        #DB['MA60'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 60)
        #DB['MA120'] = pd.stats.moments.rolling_mean(DB['Adj Close'], 120)
        DB['MA200']     = pd.stats.moments.rolling_mean(DB['Adj Close'], 200)
        DB['MA240']     = pd.stats.moments.rolling_mean(DB['Adj Close'], 240)
        DB['DateStamp'] = [ date2num(datetime.strptime(date,"%Y-%m-%d")) for date in DB['Date'] ]
        
        ###########################################################################
        Code = filename[:-4] # Trading Code
        
        
        command = "INSERT INTO YAHOO(Code, DateStamp, Date, Open, High, Low, Close, Volume, AdjClose, MA20, MA30, MA200, MA240) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        #print(command)
        
        for i in range(len(DB)):
            DateStamp = DB['DateStamp'][i]
            Date = DB['Date'][i]
            Open = DB['Open'][i]
            High = DB['High'][i]
            Low = DB['Low'][i] 
            Close = DB['Close'][i]
            Volume = int(DB['Volume'][i])
            AdjClose = DB['Adj Close'][i]
            MA20 = DB['MA20'][i]
            MA30 = DB['MA30'][i]
            MA200 = DB['MA200'][i]
            MA240 = DB['MA240'][i]
            
            cursor.execute(command,(Code, DateStamp, Date, Open, High, Low, Close, Volume, AdjClose, MA20, MA30, MA200, MA240) )
            connect.commit()
        nFiles += 1
            

