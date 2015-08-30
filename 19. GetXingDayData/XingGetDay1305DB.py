# -*- coding: utf-8 -*-

# Purpose: Xing(pystock 0.0.4a code list
# Date: 2015-08-30

import sqlite3
#from pystock_xingAPI import *

def main():
	#xing = Xing()
	#Xing("demo.ebestsec.co.kr", 20001, 1, 1, "아이디", "패스워드", "")
	
	conn = sqlite3.connect("t8430.db")
	select_query = "SELECT shcode from SHCODES_TB where gubun=0"

	t8430 = conn.cursor().execute(select_query)

	for row in t8430:
		print(row[0])

if __name__ == '__main__':
	main()