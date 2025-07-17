import scrapy
from scrape_multiweb.items import scrape_urls


class BisnisComUrlsSpider(scrapy.Spider):
    name = "bisnis.com-urls"
    allowed_domains = ["bisnis.com"]
    start_urls = ["https://www.bisnis.com/index"]

    def parse(self, response):
        articles_links = response.css("div.artItem a.artLink::attr(href)").getall()
        for link in articles_links:
            item = scrape_urls()
            item['url'] = response.urljoin(link)
            item['domain'] = response.url.split('/')[2]
            yield item

