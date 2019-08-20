import aiofiles

from core import AttrField, TextField, Item, Spider,Request,Middleware
from lxml import etree
from urllib.parse import urljoin
from core.utils import get_random_user_agent



class Crawler(Spider):
    def __int__(self):
        pass

    start_urls = ['http://news.sohu.com/']
    concurrency = 20



    async def parse(self, res):
        for item in  set(etree.HTML(res.html).xpath("//a//@href")):
            suburl = urljoin(res.url, item)
            if suburl.startswith("http"):
                headers = {
                    "User-Agent": await get_random_user_agent()
                }
                yield Request(suburl,
                              request_config=self.request_config,
                              headers=headers,
                              callback=self.parse_item,
                              metadata={})

    async def parse_item(self, res):
        for item in set(etree.HTML(res.html).xpath("//a//@href")):
            suburl = urljoin(res.url, item)
            if suburl.startswith("http") and (not "" or not None):
                print(suburl)


if __name__ == '__main__':
    Crawler.start()