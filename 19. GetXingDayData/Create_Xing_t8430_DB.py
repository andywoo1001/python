# -*- coding: utf-8 -*-

# Purpose: Xing(pystock 0.0.4a code list
# Date: 2015-08-30

import sqlite3
import sys
from pystock_xingAPI import *
import  pandas as pd


def main():
	xing = Xing()
	
	if xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "insuyu", "demo00", "") == False:
		print ('Connection Error! Exit')
		sys.exit(0)

	inblock_query_t8430 = { 't8430InBlock' : { 'gubun' : 0 } }
	t8430 = xing.query('xing.t8430', inblock_query_t8430)
	print ('number of list : %d' % len(t8430['t8430OutBlock']) )
	

	conn = sqlite3.connect("t8430.db")
	
	# Create a new table CODE_TB
	DBUtil.create_table_for_outblock(conn.cursor(), 'CODE_TB', 't8430', 't8430OutBlock', ['shcode'])
	conn.commit()
	# Submit CODE_TB
	DBUtil.insert_for_outblock(conn.cursor(), 'CODE_TB', t8430['t8430OutBlock'], place_flag = True)
	conn.commit()
	print ('CODE_TB table is created')
	conn.close()

	# Create a table for each stock AXXXXXX
"""	index = 1
	for row in t8430['t8430OutBlock']:
		gubun 	= row['gubun']
		shcode 	= row['shcode']
		hname	= row['hname']
		
		# Create a new t1305 table for each stock
		table_name = 'A'+shcode
		DBUtil.create_table_for_outblock(conn.cursor(), table_name, 't1305', 't1305OutBlock1', ['date'])
		conn.commit()
		print('%d %1s %6s %s' % (index, gubun, shcode, hname))
		index += 1
	xing.close()

	print ('Table (%d) is created in XingDB.db ' % index )"""



if __name__ == '__main__':
	main()