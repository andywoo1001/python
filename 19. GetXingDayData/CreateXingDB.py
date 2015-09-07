# -*- coding: utf-8 -*-

# Purpose: Xing(pystock 0.0.4a code list
# Date: 2015-08-30

import sqlite3
import sys
from pystock_xingAPI import *
import  pandas as pd


from datetime import datetime
import time
from time import gmtime, strftime
import sys, traceback

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

t1305_tablelist = ''
for i in range(len(t1305_struct)): 
	t1305_tablelist += t1305_struct[i][0] + ' ' + t1305_struct[i][1] 
	if(i != len(t1305_struct)-1):
	    t1305_tablelist += ','

# Create SQL Insert list
t1305_insertlist = ''
for i in range(len(t1305_struct)): 
	t1305_insertlist += t1305_struct[i][0]
	if( i != len(t1305_struct)-1):
	    t1305_insertlist += ','



def Create_t8430():
	xing = Xing()
	
	if xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "insuyu", "demo00", "") == False:
		print ('Connection Error! Exit')
		sys.exit(0)

	inblock_query_t8430 = { 't8430InBlock' : { 'gubun' : 0 } }
	t8430 = xing.query('xing.t8430', inblock_query_t8430)
	print ('number of list : %d' % len(t8430['t8430OutBlock']) )
	

	connect = sqlite3.connect("XingDB.db")
	
	# Create a new table CODE_TB
	DBUtil.create_table_for_outblock(connect.cursor(), 'CODE_TB', 't8430', 't8430OutBlock', ['shcode'])
	connect.commit()

	# Submit CODE_TB
	DBUtil.insert_for_outblock(connect.cursor(), 'CODE_TB', t8430['t8430OutBlock'], place_flag = True)
	connect.commit()
	connect.close()
	print ('CODE_TB table is created')



def Create_t1305():
	xing = Xing()
	
	if xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "insuyu", "demo00", "") == False:
		print ('Connection Error! Exit')
		sys.exit(0)

	connect = sqlite3.connect("XingDB.db")
	cursor = connect.cursor()
	DBt8430 = connect.cursor().execute("SELECT shcode, hname, gubun, etfgubun from CODE_TB").fetchall()

	print ('number of stock indices from XingDB.db : %d' % len(DBt8430) )

	startIndex 	= 0
	endIndex 	= 4 #len(DBt8430)
	for index in range(startIndex, endIndex):
		shcode 	= DBt8430[index][0] #shcode
		hname 	= DBt8430[index][1] #hname
		gubun 	= DBt8430[index][2]
		etfgubun = DBt8430[index][3]

		inblock_query_t1305 = {
			't1305InBlock' : {
				'shcode' : shcode,
				'dwmcode' : 1,
				'date' : None,
				'idx' : None,
				'cnt' : 9999
			}
		}

		Data = []
		DB = []
		while True:
			t1305 = xing.query('xing.t1305', inblock_query_t1305)

			# Add to the list
			for v in t1305['t1305OutBlock1']:
				Data.append(	(v['shcode'], v['date'], v['open'], v['high'], v['low'], v['close'], v['sign'], v['change'], v['diff'], 
					v['volume'], v['diff_vol'], v['chdegree'], v['sojinrate'], v['changerate'], v['fpvolume'], v['covolume'], v['value'],
					 v['ppvolume'], v['o_sign'], v['o_change'], v['o_diff'], v['h_sign'], v['h_change'], v['h_diff'], v['l_sign'], v['l_change'], 
					 v['l_diff'], v['marketcap'] ))

			if t1305['t1305OutBlock']['idx'].strip() == '0':
				count = len(Data)
				table_name = 'A'+shcode
				
				# Create a New Table for Code
				command = "CREATE TABLE %s (%s)" % (table_name, t1305_tablelist)
				#print(command)
				cursor.execute(command)
				
				command = "INSERT INTO %s(%s) VALUES (%s)" % (table_name, t1305_insertlist, '?,'*(len(t1305_struct)-1) + '?' )
				#print(command)
				cursor.executemany(command, Data)
				
				print ('%s %4d %06s(%4d) - %s %s %s done' % (strftime("%H:%M:%S", time.localtime()), index, shcode, count, hname, gubun, etfgubun))
				break
			else:
				inblock_query_t1305['t1305InBlock']['idx'] = t1305['t1305OutBlock']['idx']
				inblock_query_t1305['continue_query'] = Trues
	connect.close()

if __name__ == '__main__':
	Create_t8430()
	Create_t1305()
	print('Finish')
	sys.exit(0)