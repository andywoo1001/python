# ~/GitHub/python/20. Scrapy/tutorial$scrapy crawl ex1

import scrapy
class DmozSpider(scrapy.Spider): 
	name = "ex1"
	allowed_domains = ["dmoz.org"]
	start_urls = ["http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"]


	def parse(self, response):
		index = 1
		path = '/html/body/div[@class="nodViewN"]/div[@id="bd-cross"]/fieldset[@class="fieldcap"]/ul[@class="directory-url"]/li'
		for sel in response.xpath(path): # //ul/li
			title = sel.xpath('a/text()').extract()
			link = sel.xpath('a/@href').extract()
			desc = sel.xpath('text()').extract()
			print (index)
			print ('title = %s' % title)
			print ('link = %s' % link)
			print ('desc = %s\n' % desc)
			index += 1