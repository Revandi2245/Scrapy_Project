import scrapy
import json
from urllib.parse import urlparse
from scrape_multiweb.items import ScrapeMultiwebItem

class GenericSpider(scrapy.Spider):
    name = "generic_spider"

    def __init__(self, portal_config=None, selectors=None, selector_types=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load from JSON strings if passed via CLI
        if isinstance(portal_config, str):
            self.portal_config = json.loads(portal_config)
        else:
            self.portal_config = portal_config

        if isinstance(selectors, str):
            self.selectors = json.loads(selectors)
        else:
            self.selectors = selectors

        if isinstance(selector_types, str):
            self.selector_types = json.loads(selector_types)
        else:
            self.selector_types = selector_types

        self.start_urls = self.portal_config.get("seed_urls", [])
        self.domain = self.portal_config.get("domain")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_article_urls)

    def parse_article_urls(self, response):
        # Ambil selector untuk article_url_list
        article_url_selector = self._get_selector("article_url_list")

        if article_url_selector:
            urls = self._extract_with_selector(response, article_url_selector)
            for link in urls:
                yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        item = ScrapeMultiwebItem()
        item['url'] = response.url
        item['domain'] = urlparse(response.url).netloc

        for selector_type in self.selector_types:
            name = selector_type['name']
            selector_conf = self._get_selector(name)
            if selector_conf:
                value = self._extract_with_selector(response, selector_conf)
                item[name] = value

        yield item

    def _get_selector(self, type_name):
        type_id = None
        for st in self.selector_types:
            if st['name'] == type_name:
                type_id = self.selector_types.index(st) + 1
                break

        for selector in self.selectors:
            if selector['selector_type_id'] == type_id and selector['portal_id'] == self.portal_config.get('id') and selector['is_active']:
                return selector

        return None

    def _extract_with_selector(self, response, selector_conf):
        method = selector_conf.get("method")
        query = selector_conf.get("query")
        is_list = selector_conf.get("is_list", False)
        post_processing = selector_conf.get("post_processing", {})

        if method == "css":
            raw = response.css(query)
        elif method == "xpath":
            raw = response.xpath(query)
        else:
            return None

        data = raw.getall() if is_list else raw.get()

        # Post-processing
        if isinstance(data, list):
            return [self._process_text(text, post_processing) for text in data]
        elif isinstance(data, str):
            return self._process_text(data, post_processing)
        return data

    def _process_text(self, text, post_processing):
        if not isinstance(text, str):
            return text
        if post_processing.get("strip"):
            text = text.strip()
        for pair in post_processing.get("replace", []):
            old, new = pair
            text = text.replace(old, new)
        return text
