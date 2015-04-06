from scrapy.spider import Spider
from scrapy.selector import Selector
from ..items import LcboItem
from scrapy.http import Request
from scrapy.cmdline import execute
from db.oadb import OADB

class LCBOItemSpider(Spider):
	name = "lcboItem"
	allowed_domains = ["foodanddrink.ca"]

	def __init__(self):
            self.db = OADB()
            self.start_urls = self.db.getLCBOLinks()[:2]

        def closed(self, reason):
            self.db.close()

	def parse(self, response):
            sel = Selector(response)
            item = LcboItem()
            link = response.url
            dID = self.db.getID(link)
            item['ID'] = dID
            sel = Selector(response)
            item["link"]=sel.xpath('//input[@name="itemNumber"]/@value').extract()[0]
            container = sel.xpath('//td[@class="main_font"][1]')
            if container.re(r'PRODUCT DISCONTINUED') != [] or container.re(r'N/A%') != []:
                # code for discontinued
                self.db.setVisited(dID)
                return
            item["price"] = float(container.re('(?<=\$ )[\d|\.]*')[0])
            item["alc"] = float(container.re('\d+\.\d+(?=%)')[0])
            item["form"] = container.re('(?<=mL ).*(?=\r)')[0]
            amount = container.re('\dx\d')
            if amount == []:
                item["amount"] = 1
            else:
                item["amount"] = int(container.re('\d+(?=x\d+)')[0])
            item["vol"] = int(container.re('\d+(?= mL)')[0])
            item["name"] = container.xpath('//span[@class="titlefont"]/text()').extract()[0]
            if len(container.re('(?<=, )[^,]+(?=,[^,]+\d+\.\d+%)')) > 0 and"<br>" in container.re('(?<=, )[^,]+(?=,[^,]+\d+\.\d+%)')[0]:
                item["Type"] = container.re('[^,\n\s]+(?=,[^,]+\d+\.\d+%)')[0]
                item["cat1"] = container.re('(?<=, )[^,]+(?=<br>[^,]+\d+\.\d+%)')[0]
            elif "<br>" in container.re('(?<=, )[^,]+(?=<br>[^,]+\d+\.\d+%)')[0] :
                item["Type"] = container.re('[^,\n\s]+(?=<br>[^,]+\d+\.\d+%)')[0]
            else:
                item["Type"] = container.re('[^,\n\s]+(?=,[^,]+\d+\.\d+%)')[0]
                item["cat1"] = container.re('(?<=, )[^,]+(?=,[^,]+\d+\.\d+%)')[0]
                item["cat2"] = container.re('(?<=, )[^,]+(?=<br>[^,]+\d+\.\d+%)')[0]

	    yield item
            self.db.setVisited(dID)
