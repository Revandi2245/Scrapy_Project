import scrapy
from urllib.parse import urlparse
from scrape_multiweb.items import ScrapeMultiwebItem

class KompasSpiderSpider(scrapy.Spider):
    name = "kompas_spider"
    allowed_domains = ["kompas.com"]

    def __init__(self, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ScrapeMultiwebItem()
        item['domain'] = urlparse(response.url).netloc
        item['title'] = response.css("h1.read__title::text").get()
        item['description'] = response.css("meta[name='description']::attr(content)").get()
        item['body'] = ' '.join(response.css("div.read__content p::text").getall())
        item['image'] = response.css("meta[property='og:image']::attr(content)").get()
        item['author'] = (response.css("meta[property='content_author']::attr(content)") or 
                            response.css("meta[property='content_editor']::attr(content)") or
                            response.css("div.credit-title-nameEditor::text")).get().strip()
        # item['published_date'] = response.css("div.read__time::text").get(default="Unknown")
        item['published_date'] = response.css('meta[property="article:published_time"]::attr(content)').get(default="Unknown")
        item['language'] = 'id'
        yield item
