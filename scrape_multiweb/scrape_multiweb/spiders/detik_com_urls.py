import scrapy
from scrape_multiweb.items import scrape_urls

class DetikComUrlsSpider(scrapy.Spider):
    name = "detik.com-urls"
    allowed_domains = ["detik.com"]
    start_urls = ["https://news.detik.com/indeks"]

    def parse(self, response):
        articles_links = response.css("article.list-content__item a.media__link::attr(href)").getall()
        for link in articles_links:
            item = scrape_urls()
            item['url'] = response.urljoin(link)
            item['domain'] = response.url.split('/')[2]
            yield item
