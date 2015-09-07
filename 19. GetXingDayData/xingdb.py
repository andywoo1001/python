# -*- coding: utf-8 -*-

# Purpose: Xing(pystock 0.0.4a code list
# Date: 2015-08-30

import sqlite3
from pystock_xingAPI import *
import  pandas as pd

from datetime import datetime
import time
from time import gmtime, strftime

xing = Xing()
	
if xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "insuyu", "demo00", "") == False:
	print ('Connection Error! Exit')
	sys.exit(0)



t1305Column = ['volume', 'value', 'sojinrate', 'high', 'covolume', 'l_change', 'o_diff', 'marketcap', 'low', 'h_sign', 'chdegree', 'shcode', 
'o_change', 'l_diff', 'diff', 'date', 'open', 'sign', 'h_diff', 'h_change', 'ppvolume', 'l_sign', 'changerate', 'fpvolume',  'o_sign', 'change', 'close', 'diff_vol']

#conn = sqlite3.connect("XingDB.db")
t8430 = conn.cursor().execute("SELECT shcode, hname, gubun, etfgubun from CODE_TB").fetchall()
print ('number of codes from t8430.db : %d' % len(t8430) )


startIndex = 0
endIndex = len(t8430)
for index in range(startIndex, endIndex):
	shcode 	= t8430[index][0] #shcode
	hname 	= t8430[index][1] #hname
	gubun 	= t8430[index][2]
	etfgubun = t8430[index][3]

	table_name = 'A'+shcode
	DBUtil.create_table_for_outblock(conn.cursor(), table_name, 't1305', 't1305OutBlock1', ['date'])
	conn.commit()

	inblock_query_t1305 = {
		't1305InBlock' : {
			'shcode' : shcode,
			'dwmcode' : 1,
			'date' : None,
			'idx' : None,
			'cnt' : 9999
		}
	}

	DB = []
	count = 1
	while True:
		t1305 = xing.query('xing.t1305', inblock_query_t1305)
		#DBUtil.insert_for_outblock(conn.cursor(), table_name, t1305['t1305OutBlock1'], place_flag = False)
		
		for row in t1305['t1305OutBlock1']:
			#print(str(count) + '. ' + str(row['date']))
			DB.append([ row['volume'], row['value'], row['sojinrate'], row['high'], row['covolume'], row['l_change'], row['o_diff'], row['marketcap'], row['low'], row['h_sign'], row['chdegree'], row['shcode'], row['o_change'], row['l_diff'], row['diff'], row['date'], row['open'], row['sign'], row['h_diff'], row['h_change'], row['ppvolume'], row['l_sign'], row['changerate'], row['fpvolume'],  row['o_sign'], row['change'], row['close'], row['diff_vol'] ])
			count += 1

		if t1305['t1305OutBlock']['idx'].strip() == '0':
			DB = pd.DataFrame(DB, columns=t1305Column)
			DB.to_csv(shcode + '.csv')
			print ('%s %4d %06s(%4d) - %s %s %s done' % (strftime("%H:%M:%S", time.localtime()), index, shcode, count, hname, gubun, etfgubun))
			break
		else:
			inblock_query_t1305['t1305InBlock']['idx'] = t1305['t1305OutBlock']['idx']
			inblock_query_t1305['continue_query'] = Trues

