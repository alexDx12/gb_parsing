import scrapy
from scrapy.http import HtmlResponse
from productparser.items import ProductparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [
            f'https://leroymerlin.ru/search/?q={search}'
        ]

    def parse(self, response):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_products)

    def parse_products(self, response: HtmlResponse):
        loader = ItemLoader(item=ProductparserItem(), response=response)
        loader.add_xpath('_id', '//span[@itemprop="sku"]/@content')
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('currency', '//span[@slot="currency"]/text()')
        loader.add_xpath('unit', '//span[@slot="unit"]/text()')
        loader.add_xpath('feature_names', '//dl/div/dt/text()')
        loader.add_xpath('feature_values', '//dl/div/dd/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('photos', '//picture[@slot]/source[1]/@srcset')
        yield loader.load_item()