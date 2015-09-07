# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
import time
import re
from time import gmtime, strftime
from urllib2 import HTTPError
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup

def Download_html(url, filename):
	f = open(filename, 'wb')
	try:
		html = urllib2.urlopen(url)	
	except HTTPError as e:
		return None
	f.write(html.read())
	f.close()


connect = sqlite3.connect('InfoStock.db')
cursor = connect.cursor()

cursor.execute('SELECT * FROM INFOSTOCK ')
#cursor.fetchall()

count = 1
for row in cursor.fetchall():
	date, url, title = row
	date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
	date_str = date_obj.strftime("%Y%m%d_%H%M_")
	idx 	= re.findall("uid=(\d\d\d+)", url)
	date_str = date_str + idx[0] + '.html'
	print ('[%s] %d %s %s' % (strftime("%H:%M:%S", time.localtime()), count, date_str, url))
	Download_html(str(url), date_str )
	count += 1