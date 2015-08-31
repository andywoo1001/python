# -*- coding: utf-8 -*-

# Purpose: Xing(pystock 0.0.4a code list
# Date: 2015-08-30

import sqlite3
from pystock_xingAPI import *

def main():
	xing = Xing()
	
	if xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "insuyu", "demo00", "") == False:
		print ('Connection Error! Exit')
		sys.exit(0)

	conn = sqlite3.connect("t8430.db")
	
	select_query = "SELECT shcode from CODE_TB"
	ret = conn.cursor().execute(select_query)
		
	for row in ret:
		shcode = row[0]
		table_name = 'A'+shcode
		DBUtil.create_table_for_outblock(conn.cursor(), table_name, 't8413', 't8413OutBlock1', ['date'])
		conn.commit()

		print ('Code:%s, Table:%s' % (shcode, table_name) )

		inblock_query_t8413 = {
			't8413InBlock' : {
				'shcode' : shcode,
				'gubun' : 2,
				'qrycnt' : None, 
				'sdate' : "19800101",
				'edate' : "99999999",
				'cts_date' : None, 
				'comp_yn' : 'Y'
			},
			'continue_query':False
		}
		while True:
			data = xing.query('xing.t8413', inblock_query_t8413)
			DBUtil.insert_for_outblock(conn.cursor(), table_name, data['t8413OutBlock1'], place_flag = False)

			if not data['t8413OutBlock']['cts_date'].strip():
				conn.commit()
				break
			inblock_query_t8413['continue_query'] = True
			inblock_query_t8413['t8413InBlock']['cts_date'] = data['t8413OutBlock']['cts_date']

if __name__ == '__main__':
	main()