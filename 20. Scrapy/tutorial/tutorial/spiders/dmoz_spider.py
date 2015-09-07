from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field


class DmozItem(Item):
	number = Field()
	question = Field()
	answer = Field()


class DmozSpider(BaseSpider):
	name = "dmoz"
	allowed_domains = ["2345.com"]
	start_urls = ["http://www.2345.com/jzw/1.htm"]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)

		rows = hxs.select('//body/center/table[2]/tr')
		for row in rows:
			item = DmozItem()
			try:
				item['number'] = row.select(".//td[1]/p/font/text()").extract()[0]
				item['question'] = row.select(".//td[2]/font/text()").extract()[0]
				item['answer'] = row.select(".//td[3]/p/input/@onclick").extract()[0][13:-2]
			except:
				continue
			yield item