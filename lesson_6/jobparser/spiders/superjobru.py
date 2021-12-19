import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="icMQ_ bs_sM _3ze9n _1M2AW f-test-button-dalshe f-test-link-Dalshe"]').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[ @class ="f-test-search-result-item"]//a[@ target="_blank" and contains(@href, "html")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath("//h1/following-sibling::span/span//text()").getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item