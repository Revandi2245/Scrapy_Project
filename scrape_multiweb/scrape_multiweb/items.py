# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class scrape_urls(scrapy.Item):
    url = scrapy.Field()
    domain = scrapy.Field()

class ScrapeMultiwebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    body = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    published_date = scrapy.Field()
    language = scrapy.Field()