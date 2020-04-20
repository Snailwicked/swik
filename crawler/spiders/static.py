import scrapy
from urllib.parse import urljoin
from utils.headers import random_headers

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://news.sohu.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in set(response.xpath("//a//@href")):
            suburl = urljoin(response.url, item.get())
            if suburl.startswith("http") and (not "" or not None):
                yield scrapy.Request(url=suburl, headers=random_headers,callback=self.parse_item)

    def parse_item(self, response):
        for item in set(response.xpath("//a//@href")):
            suburl = urljoin(response.url, item.get())
            if suburl.startswith("http") and (not "" or not None):
                print(suburl)


