# ~/GitHub/python/20. Scrapy/tutorial$scrapy crawl ex2
# scrapy shell "http://www.2345.com/jzw/1.htm"
# -*- coding: utf-8 -*-


import scrapy
class DmozSpider(scrapy.Spider): 
	name = "ex2"
	allowed_domains = ["dmoz.org"]
	start_urls = ["http://www.2345.com/jzw/1.htm"]


	def parse(self, response):
		index = 1
		path = '/html/body/div[@class="jzw_container"]/ul/li/span[@class="table_left"]'
		for sel in response.xpath(path): # //ul/li
			#title = sel.xpath('a/text()').extract()
			#link = sel.xpath('a/@href').extract()
			desc = sel.xpath('text()').extract()
			print (index)
			#print ('title = %s' % title)
			#print ('link = %s' % link)
			print ('desc = %s\n' % desc[0])
			index += 1