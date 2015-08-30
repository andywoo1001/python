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
		
	for row in t8430['t8430OutBlock']:
		print('%1s,%6s,%s' % (row['gubun'], row['shcode'], row['hname']) )
   
	conn = sqlite3.connect("t8430.db")
	DBUtil.create_table_for_outblock(conn.cursor(), 'SHCODES_TB', 't8430', 't8430OutBlock', ['shcode'])
	conn.commit()

	DBUtil.insert_for_outblock(conn.cursor(), 'SHCODES_TB', t8430['t8430OutBlock'], place_flag = True)
	conn.commit()

	xing.close()



if __name__ == '__main__':
	main()