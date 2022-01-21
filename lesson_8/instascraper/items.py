# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstascraperItem(scrapy.Item):
    # define the fields for your item here like:
    friend_id = scrapy.Field()
    friend_name = scrapy.Field()
    full_name = scrapy.Field()
    username = scrapy.Field()
    u_type = scrapy.Field()
    _id = scrapy.Field()

