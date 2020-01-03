from urllib.parse import urljoin
from config.conf import get_algorithm
from utils import xPathTexts
import time
from collections import defaultdict

args = get_algorithm()
from db.redis_db import Url_Parameter
url_storage = Url_Parameter()
from utils.base_utils import bloomfilter
class Crawler:
    def __init__(self):
        self.xpath = xPathTexts()
        self.brief =[]


    def run(self,parameter):
        self.parameter = parameter
        self.rule = self.parameter['rule']
        self.limit = int(self.rule["deep_limit"]) if self.rule["deep_limit"] !="" else 1
        self.xpath_urls([self.parameter["url"]])

    def get_hrefs(self,url):
        self.xpath.set_parameter(url)
        urls = set(self.xpath.get_contents("//a//@href"))
        temp = set()
        for item in urls:
            suburl = urljoin(url, item)
            if suburl.startswith("http"):
                temp.add(suburl)
        return temp

    def xpath_urls(self, urls):
        url_filter = bloomfilter.filter(args["news_url"])

        for url in urls:
            for item in self.get_hrefs(url):
                if url_filter.filter_text(item):
                    self.brief.append(item)
                else:
                    for item in self.get_hrefs(item):
                        if url_filter.filter_text(item):
                            self.brief.append(item)
                        else:
                            continue
        url_filter.tofile()

    def process(self):
        return self.brief


class Crawleruning(Crawler):

    def __init__(self):
        super(Crawleruning, self).__init__()

    def start(self):
        self.run(self.parameters)

    def set_parameter(self,parameter):
        self.parameters = parameter


if __name__ == '__main__':
    # parameter = {'url': 'http://www.legalweekly.cn/', 'rule': {'filter_rule': '', 'selector': 'xpath选择器', 'deep_limit': 1, 'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}}
    # crawler = Crawleruning()
    # crawler.set_parameter(parameter)
    # crawler.start()
    # url_storage.store_parameter("requests", "test")

    print(url_storage.fetch_llen("requests"))
    # key = 1
    # while key:
    #     urls = url_storage.fetch_parameters("requests")
    #     if urls:
    #         for url in urls:
    #             print(url)
    #     else:
    #         key = 0
