import sys
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from productparser import settings
from productparser.spiders.leroymerlinru import LeroymerlinruSpider

if __name__ == '__main__':
    crawlwer_settings = Settings()
    crawlwer_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawlwer_settings)
    # process.crawl(LeroymerlinruSpider, search=sys.argv[1])
    process.crawl(LeroymerlinruSpider, search='пакеты для мусора')
    process.start()

