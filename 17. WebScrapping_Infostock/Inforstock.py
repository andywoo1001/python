# -*- coding: utf-8 -*-
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time



def Download_html(url, filename):
	f = open(filename, 'wb')
	try:
		html = urllib2.urlopen(url)	
	except HTTPError as e:
		return None
	f.write(html.read())
	f.close()

def Parse_Infostock_html(url, page):
	try:
		html = urllib2.urlopen(url)	
	except HTTPError as e:
		return None

	#print( unicode(html.read(), "euc-kr").encode("utf-8") )
	
	try:
		bsObj = BeautifulSoup(html.read())
	except AttributeError as e:
		return None

	tr_list = bsObj.find('table').findAll('tr')
	
	count = 0
	for tr in tr_list:
		td_title = tr.find('td', {"class":"title"})
		td_date = tr.find('td', {"class":"t_11_brown"})
		if (td_title != None and td_date != None):
			# Ignore the duplication of first item
			if count == 0:
				count += 1
				continue

			text_time = td_date.get_text()
			text_time = text_time.replace('.','-')
			text_link = td_title.find('a').get('href') #.attrs['href']
			# encode the string as utf-8 in code
			text_title = td_title.get_text() #.encode('utf-8')
			text_title = unicode(text_title)

			#print (count, text_time, text_title)
			print ('Page%d-%d %s %s' % (page,count, text_time, text_title) )

			cursor.execute("INSERT INTO INFOSTOCK VALUES (?,?,?)", (text_time, text_link, text_title) )
			connect.commit()

			count += 1


if __name__ == "__main__":
	connect = sqlite3.connect('InfoStock.db')
	cursor = connect.cursor()
	cursor.execute("CREATE TABLE INFOSTOCK(date TEXT, url TEXT, title TEXT)")

	for page in range(4136):
		link = 'http://vip.mk.co.kr/newSt/news/news_list.php?p_page=%d&sCode=122&termDatef=&search=&topGubun=' % (page+1)
		Parse_Infostock_html(link, page)