from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy import settings as SS
from bItems.beerItem.spiders.beerItems import BeerItems
from scrapy.utils.project import get_project_settings

spider = BeerItems()
settings = SS.Settings({"ITEM_PIPELINES":{'bItems.beerItem.pipelines.BeerPipeline':300}})
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run() # the script will block here until the spider_closed signal was sent
