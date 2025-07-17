import scrapy
from scrape_multiweb.items import scrape_urls

class BogorDiswayIdUrlsSpider(scrapy.Spider):
    name = "bogor.disway.id_urls"
    allowed_domains = ["diswaybogor.id"]
    start_urls = ["https://bogor.disway.id/network/list-network"]

    def parse(self, response):
        articles_links = response.css("li a::attr(href)").getall()
        for link in articles_links:
            item = scrape_urls()
            item['url'] = response.urljoin(link)
            yield item

