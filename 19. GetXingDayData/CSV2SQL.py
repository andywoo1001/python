import pandas as pd
import os
import time
from datetime import datetime
from matplotlib.dates import date2num
import sqlite3

# Create NEW SQL database
connect = sqlite3.connect('XingDB.db')
cursor = connect.cursor()

# For All Files in PATH
nFiles = 0
for filename in os.listdir('./'):
    # Find only *.csv files
    if filename.endswith(".csv"):
        print ("[%d] %s" % (nFiles, filename))
        # Load CVS to Database
        DB = pd.read_csv(filename)
    
        # Generate Moving Average Data
        DB['MA20'] = pd.stats.moments.rolling_mean(DB['close'], 20)
        DB['MA30'] = pd.stats.moments.rolling_mean(DB['close'], 30)
        DB['MA60'] = pd.stats.moments.rolling_mean(DB['close'], 60)
        DB['MA120'] = pd.stats.moments.rolling_mean(DB['close'], 120)
        DB['MA200'] = pd.stats.moments.rolling_mean(DB['close'], 200)
        DB['MA240'] = pd.stats.moments.rolling_mean(DB['close'], 240)
        
        ###########################################################################
        Code = filename[:-4] # Trading Code
        
        table_name = 'A' + Code

        # Create a New Table for Code
        # DateStamp(REAL) | Date(TEXT) | Open(REAL) | High(REAL) | Low(REAL) 
        #    | Close(REAL) | Volume(REAL) | AdjClose(REAL) | MA20(REAL) | MA30(REAL) | MA200(REAL) | MA240 (REAL)
        command = "CREATE TABLE %s (Code TEXT, DateStamp INT, Date TEXT, Open REAL, High REAL, Low REAL, Close REAL, Volume INT, AdjClose REAL, MA20 REAL, MA30 REAL, MA200 REAL, MA240 REAL)" % table_name
        print(command)
        cursor.execute(command)

        command = "INSERT INTO %s(Code, DateStamp, Date, Open, High, Low, Close, Volume, AdjClose, MA20, MA30, MA200, MA240) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)" % table_name
        print(command)
        
        volume  value   sojinrate   high    covolume    l_change    o_diff  marketcap   low h_sign  chdegree    shcode  o_change    l_diff  diff    date    open    sign    h_diff  h_change    ppvolume    l_sign  changerate  fpvolume    o_sign  change  close   diff_vol

        종목코드,shcode,shcode,char,6;
        날짜,date,date,char,8;
        시가,open,open,long,8;
        고가,high,high,long,8;
        저가,low,low,long,8;
        종가,close,close,long,8;
        전일대비구분,sign,sign,char,1;
        전일대비,change,change,long,8;
        등락율,diff,diff,float,6.2;
        누적거래량,volume,volume,long,12;
        거래증가율,diff_vol,diff_vol,float,10.2;
        체결강도,chdegree,chdegree,float,6.2;
        소진율,sojinrate,sojinrate,float,6.2;
        회전율,changerate,changerate,float,6.2;
        외인순매수,fpvolume,fpvolume,long,12;
        기관순매수,covolume,covolume,long,12;
        누적거래대금(단위:백만),value,value,long,12;
        개인순매수,ppvolume,ppvolume,long,12;
        시가대비구분,o_sign,o_sign,char,1;
        시가대비,o_change,o_change,long,8;
        시가기준등락율,o_diff,o_diff,float,6.2;
        고가대비구분,h_sign,h_sign,char,1;
        고가대비,h_change,h_change,long,8;
        고가기준등락율,h_diff,h_diff,float,6.2;
        저가대비구분,l_sign,l_sign,char,1;
        저가대비,l_change,l_change,long,8;
        저가기준등락율,l_diff,l_diff,float,6.2;
        시가총액(단위:백만),marketcap,marketcap,long,12;

        shcode text,

        volume integer,
        value integer,
        sojinrate real,
        high integer,
        covolume integer,
        l_change integer,
        o_diff real,
        marketcap integer,
        low integer,


        h_sign text,

  o_change integer,
  
  sign text,
  diff_vol real,
  
  l_sign text,
  o_sign text,

  h_change integer,
  changerate real,
  date text,
  
  open integer,
  l_diff real,
  change integer,
  ppvolume integer,
  fpvolume integer,

  chdegree real,
  diff real,
  h_diff real,
 

  
  close integer
);

        """for i in range(len(DB)):
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
            connect.commit()"""
        nFiles += 1
            

