from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy import settings as SS
from bLinks.beerLink.spiders.beerLinks import BeerLinks
from scrapy.utils.project import get_project_settings
from db.oadb import OADB

spider = BeerLinks()
settings = SS.Settings({"ITEM_PIPELINES":{'bLinks.beerLink.pipelines.LinkPipeline':300}})
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run() # the script will block here until the spider_closed signal was sent
