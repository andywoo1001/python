import sqlite3
from pystock_xingAPI import *
import  pandas as pd

xing = Xing()

xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "insuyu", "demo00", "")

inblock_query_t8430 = { 't8430InBlock' : { 'gubun' : 0 } }
t8430 = xing.query('xing.t8430', inblock_query_t8430)

t1305Column = ['volume', 'value', 'sojinrate', 'high', 'covolume', 'l_change', 'o_diff', 'marketcap', 'low', 'h_sign', 'chdegree', 'shcode', 
'o_change', 'l_diff', 'diff', 'date', 'open', 'sign', 'h_diff', 'h_change', 'ppvolume', 'l_sign', 'changerate', 'fpvolume', 
'o_sign', 'change', 'close', 'diff_vol']

list = 1
for row in t8430['t8430OutBlock']:
	shcode = row['shcode']
	hname = row['hname']

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
		for row in t1305['t1305OutBlock1']:
			#print(str(count) + '. ' + str(row['date']))
			DB.append([ row['volume'], row['value'], row['sojinrate'], row['high'], row['covolume'], row['l_change'], row['o_diff'], row['marketcap'], row['low'], row['h_sign'], row['chdegree'], row['shcode'], row['o_change'], row['l_diff'], row['diff'], row['date'], row['open'], row['sign'], row['h_diff'], row['h_change'], row['ppvolume'], row['l_sign'], row['changerate'], row['fpvolume'],  row['o_sign'], row['change'], row['close'], row['diff_vol'] ])
			count += 1

		if t1305['t1305OutBlock']['idx'].strip() == '0':
			DB = pd.DataFrame(DB, columns=t1305Column)
			DB.to_csv(shcode+'_'+ hname + '.csv')
			print ('%d. %s(%s) (%d) is read' % (list, hname, shcode, count))
			list += 1
			break
		else:
			inblock_query_t1305['t1305InBlock']['idx'] = t1305['t1305OutBlock']['idx']
			inblock_query_t1305['continue_query'] = True