# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import MapCompose, TakeFirst
import scrapy

def clear_price(value):
    value = value.replace(' ', '')
    try:
        return int(value)
    except:
        return value

def clear_feature_values(feature_value):
    clear_feature_value = feature_value.replace('\n', '').strip()
    return clear_feature_value

class ProductparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    currency = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    feature_names = scrapy.Field()
    feature_values = scrapy.Field(input_processor=MapCompose(clear_feature_values))
    features = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()

