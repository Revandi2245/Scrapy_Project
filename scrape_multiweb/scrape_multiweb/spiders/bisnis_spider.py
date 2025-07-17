import scrapy
from urllib.parse import urlparse
from scrape_multiweb.items import ScrapeMultiwebItem

class BisnisSpiderSpider(scrapy.Spider):
    name = "bisnis_spider"
    allowed_domains = ["bisnis.com"]

    def __init__(self, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ScrapeMultiwebItem()
        item['domain'] = urlparse(response.url).netloc
        item['title'] = (response.css("h1.detailsTitleCaption::text").get() or
                         response.css("h1.text-jet::text").get())
        item['description'] = response.css("meta[name='description']::attr(content)").get()
        item['body'] = ' '.join(response.css("article.detailsContent p::text").getall())
        item['image'] = response.css("meta[property='og:image']::attr(content)").get()
        item['author'] = (response.css("meta[name='author']::attr(content)").get() or 
                            response.css("div.authorName strong::text").get() or
                            response.css("div.authorNames a::text").get())
        item['published_date'] = (response.css("meta[name='publishdate']::attr(content)") or 
                                    response.css("div.detailsAttributeDates::text") or
                                    response.css('p.authorTime::text')).get(default="Unknown").strip()
        item['language'] = 'id'
        yield item