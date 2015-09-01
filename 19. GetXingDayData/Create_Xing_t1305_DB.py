# -*- coding: utf-8 -*-

# Purpose: Xing(pystock 0.0.4a code list
# Date: 2015-08-30

import sqlite3
from pystock_xingAPI import *
import  pandas as pd

from datetime import datetime
import time
from time import gmtime, strftime


def main():
	xing = Xing()
	
	if xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "insuyu", "demo00", "") == False:
		print ('Connection Error! Exit')
		sys.exit(0)
	else:
		print ('Connection successful')

	# Read from t8430 database
	conn = sqlite3.connect("XingDB.db")
	t8430 = conn.cursor().execute("SELECT shcode, hname from CODE_TB").fetchall()
	print ('number of codes from t8430.db : %d' % len(t8430) )

	
	startIndex = 0
	endIndex = 1

	for index in range(startIndex, endIndex):
		shcode 	= t8430[index][0] #shcode
		hname 	= t8430[index][1] #hname
		table_name = 'A'+shcode
		#print('%d %s %s %s' % (index, table_name, shcode, hname))
		
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

		count = 1
		while True:
			t1305 = xing.query('xing.t1305', inblock_query_t1305)
			DBUtil.insert_for_outblock(conn.cursor(), table_name, t1305['t1305OutBlock1'], place_flag = False)
			count += len(t1305['t1305OutBlock1'])

			if t1305['t1305OutBlock']['idx'].strip() == '0':
				print ('%s %4d %s(%s) (%d) is read' % ( strftime("%H:%M:%S", time.localtime()), index, hname, shcode, count))
				#print ('%d. %s(%s) (%d) is read' % (index, hname, shcode, count))
				break
			else:
				inblock_query_t1305['t1305InBlock']['idx'] = t1305['t1305OutBlock']['idx']
				inblock_query_t1305['continue_query'] = True
	print ('Finished work')


if __name__ == '__main__':
	main()