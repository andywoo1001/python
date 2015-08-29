# -*- coding: utf-8 -*-


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

def Parse_Infostock_html(url, page):
	try:
		html = urllib2.urlopen(url)	
	except HTTPError as e:
		return None

	#print( unicode(html.read(), "euc-kr").encode("utf-8") )
	
	try:
		bsObj = BeautifulSoup(html.read())
		title = bsObj.body.h1
	except AttributeError as e:
		return None

	count = 1
	tr_list = bsObj.find('table').findAll('tr')
	len(tr_list)
	for tr in tr_list:
		title_class = tr.find('td', {"class":"title"})
		date_class = tr.find('td', {"class":"t_11_brown"})
		
		if( title_class != None and date_class != None):
			time = date_class.get_text()
			link = title_class.find('a').get('href') #.attrs['href']
			# encode the string as utf-8 in code
			title = title_class.get_text() #.encode('utf-8')
			Filename = "P%04d_%02d_" % (page, count) + time + '.html'
			Download_html(link, Filename)
			print(Filename)
			count += 1


if __name__ == "__main__":
	for page in range(1,2):
		link = 'http://vip.mk.co.kr/newSt/news/news_list.php?p_page=%d&sCode=122&termDatef=&search=&topGubun=' % page
		Parse_Infostock_html(link, page)

#Download_html('http://vip.mk.co.kr/newSt/news/news_list.php?p_page=1&sCode=122&termDatef=&search=&topGubun=', 'page1.html')

