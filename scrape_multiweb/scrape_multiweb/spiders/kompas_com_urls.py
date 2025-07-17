import scrapy
from scrape_multiweb.items import scrape_urls

class KompasComUrlsSpider(scrapy.Spider):
    name = "kompas.com-urls"
    allowed_domains = ["kompas.com"]
    start_urls = ["https://indeks.kompas.com/?site=news"]

    def parse(self, response):
        articles_links = response.css("div.articleItem a.article-link::attr(href)").getall()
        for link in articles_links:
            item = scrape_urls()
            item['url'] = response.urljoin(link)
            item['domain'] = response.url.split('/')[2]
            yield item