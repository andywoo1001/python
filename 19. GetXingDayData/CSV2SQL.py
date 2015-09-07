# -*- coding: utf-8 -*-

# Purpose: Xing(pystock 0.0.4a code list
# Date: 2015-08-30

import pandas as pd
import os
import time
from datetime import datetime
from matplotlib.dates import date2num
import sqlite3
from datetime import datetime
import time
from time import gmtime, strftime


t1305_struct  = [ 
	['shcode',      'TEXT', '종목코드',    'char', '6' ],
	['date',        'TEXT', '날짜',       'char','8'],
	['open',        'INT',  '시가',       'long', '8'],
	['high',        'INT',  '고가',       'long', '8'], 
	['low',         'INT',  '저가',       'long','8'],
	['close',       'INT',  '종가',       'long','8'],
	['sign',        'TEXT', '전일대비구분', 'char','1'],
	['change',      'INT',  '전일대비',    'long','8'],
	['diff',        'REAL', '등락율',      'float','6.2'],
	['volume',      'INT',  '누적거래량',    'long','12'],
	['diff_vol',    'REAL', '거래증가율',    'float','10.2'],
	['chdegree',    'REAL', '체결강도',     'float','6.2'],
	['sojinrate',   'REAL', '소진율',      'float','6.2'],
	['changerate',  'REAL', '회전율',      'float','6.2'],
	['fpvolume',    'INT',  '외인순매수',    'long','12'],
	['covolume',    'INT',  '기관순매수',    'long','12'],
	['value',       'INT',  '누적거래대금(단위:백만)','long','12'],
	['ppvolume',    'INT',  '개인순매수',    'long','12'],
	['o_sign',      'TEXT', '시가대비구분',   'char','1'],
	['o_change',    'INT',  '시가대비',     'long','8'],
	['o_diff',      'REAL', '시가기준등락율',  'float','6.2'],
	['h_sign',      'TEXT', '고가대비구분',   'char','1'],
	['h_change',    'INT',  '고가대비',     'long','8'],
	['h_diff',      'REAL', '고가기준등락율',  'float','6.2'],
	['l_sign',      'TEXT', '저가대비구분',   'char','1'], 
	['l_change',    'INT',  '저가대비',     'long','8'],
	['l_diff',      'REAL', '저가기준등락율', 'float','6.2'],
	['marketcap',   'INT',  '시가총액(단위:백만)','long','12'],
]

# Create SQL table list
t1305_tablelist = ''
for i in range(len(t1305_struct)): 
	t1305_tablelist += t1305_struct[i][0] + ' ' + t1305_struct[i][1] + ','
	#if(i != len(t1305_struct)-1):
	#    t1305_tablelist += ','
t1305_tablelist += 'MA20 REAL, MA30 REAL, MA60 REAL, MA120 REAL, MA200 REAL, MA240 REAL'
#print (t1305_tablelist)

# Create SQL Insert list
t1305_insertlist = ''
for i in range(len(t1305_struct)): 
	t1305_insertlist += t1305_struct[i][0] + ','
	#if( i != len(t1305_struct)-1):
	#    t1305_insertlist += ','
t1305_insertlist += 'MA20, MA30, MA60, MA120, MA200, MA240'
#print (t1305_insertlist)


# Create NEW SQL database
connect = sqlite3.connect('XingDB.db')
cursor = connect.cursor()

# For All Files in PATH
nFiles = 0
for filename in os.listdir('./'):
	# Find only *.csv files
	if filename.endswith(".csv"):
		print ("%s [%d] %s" % (strftime("%H:%M:%S", time.localtime()), nFiles, filename))
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
		command = "CREATE TABLE %s (%s)" % (table_name, t1305_tablelist)
		#print(command)
		cursor.execute(command)
		print ('CREATE table')

		command = "INSERT INTO %s(%s) VALUES (%s)" % (table_name, t1305_insertlist, '?,'*(len(t1305_struct)+5) + '?' )
		#print(command)
		print ('INSERT ')

		for i in range(len(DB)):
			shcode      = '0'*(6-len(DB['shcode'][i])) + DB['shcode'][i]
			date        = '%8s' % DB['date'][i]   
			open        = '%8d' % DB['open'][i]
			high        = '%8d' % DB['high'][i]
			low         = '%8d' % DB['low'][i]
			close       = '%8d' % DB['close'][i]
			sign        = '%1s' % DB['sign'][i]
			change      = '%8d' % DB['change'][i]
			diff        = '%6.2f' % DB['diff'][i]
			volume      = '%12d' % DB['volume'][i]
			diff_vol    = '%10.2f' % DB['diff_vol'][i]
			chdegree    = '%6.2f' % DB['chdegree'][i]
			sojinrate   = '%6.2f' % DB['sojinrate'][i]
			changerate  = '%6.2f' % DB['changerate'][i]
			fpvolume    = '%12d' % DB['fpvolume'][i]
			covolume    = '%12d' % DB['covolume'][i]
			value       = '%12d' % DB['value'][i]
			ppvolume    = '%12d' % DB['ppvolume'][i]
			o_sign      = '%1s' % DB['o_sign'][i]
			o_change    = '%8d' % DB['o_change'][i]
			o_diff      = '%6.2f' % DB['o_diff'][i]
			h_sign      = '%1s' % DB['h_sign'][i]
			h_change    = '%8d' % DB['h_change'][i]
			h_diff      = '%6.2d' % DB['h_diff'][i]
			l_sign      = '%1s' % DB['l_sign'][i]
			l_change    = '%8d' % DB['l_change'][i]
			l_diff      = '%6.2f' % DB['l_diff'][i]
			marketcap   = '%12d' % DB['marketcap'][i]
			MA20        =  DB['MA20'][i]
			MA30        =  DB['MA30'][i]
			MA60        =  DB['MA60'][i]
			MA120       =  DB['MA120'][i]
			MA200       =  DB['MA200'][i]
			MA240       =  DB['MA240'][i]
		
			cursor.execute(command, (shcode,date,open,high,low,close,sign,change,diff,volume,diff_vol,chdegree,sojinrate,changerate,fpvolume,covolume,value,ppvolume,o_sign,o_change,o_diff,h_sign,h_change,h_diff,l_sign,l_change,l_diff,marketcap,MA20, MA30, MA60, MA120, MA200, MA240) )
		connect.commit()
		print ('done \n')

		nFiles += 1
			

