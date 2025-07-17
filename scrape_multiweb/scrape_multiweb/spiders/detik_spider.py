import scrapy
from urllib.parse import urlparse
from scrape_multiweb.items import ScrapeMultiwebItem

class DetikSpiderSpider(scrapy.Spider):
    name = "detik_spider"
    allowed_domains = ["detik.com"]
    
    def __init__(self, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ScrapeMultiwebItem()
        item['domain'] = urlparse(response.url).netloc
        item['title'] = response.css("h1.detail__title::text").get()
        item['description'] = response.css("meta[name='description']::attr(content)").get()
        item['body'] = ' '.join(response.css("div.detail__body p::text").getall())
        item['image'] = response.css("meta[property='og:image']::attr(content)").get()
        item['author'] = (response.css("meta[property='author']::attr(content)") or 
                            response.css("div.detail__author::text")).get()
        item['published_date'] = response.css("meta[name='publishdate']::attr(content)").get(default="Unknown")
        item['language'] = 'id'
        yield item
