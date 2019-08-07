import asyncio
import re
import urllib.parse
from lxml import etree
from urllib.parse import urljoin
from core.headers import random_headers
from utils.spiderutils.xpathtexts import xPathTexts
import queue

class QueueUtil:
    def __init__(self):
        self.queue = queue.Queue()

    def put(self, data):
        self.queue.put(data)

    def get(self):
        while not self.queue.empty():
            if self.queue.qsize() < 10:
                import time
                time.sleep(5)
            yield self.queue.get()


class Crawler:
    def __init__(self):
        self.todo = set()
        self.busy = set()
        self.done = {}
        self.dataset = set()
        self.xpath = xPathTexts()

    def run(self,parameter):
       self.parameter = parameter
       self.xpath_urls([self.parameter["url"]])


    def xpath_urls(self, urls):
        for url in urls:
            self.xpath.set_parameter(url)
            urls = self.xpath.get_contents("//a//@href")

            TEMP = []
            for item in urls:
                try:
                    suburl = urljoin(url, item)
                    if suburl.startswith("http"):
                        result = re.findall(self.parameter['re_Rule'], url)
                        if result:
                            print(result)
                        else:
                            if len(self.dataset)>int(self.parameter['limit']):
                               break
                            elif suburl not in self.dataset:
                                self.dataset.add(suburl)
                                TEMP.append(suburl)
                except:
                    print("网址不同源")
            self.xpath_urls(TEMP)

    def process(self, url):
        print(url)


class Crawleruning(Crawler):

    def __init__(self):
        super(Crawleruning, self).__init__()

    def start(self):
        for parameter in self.parameters:
            self.run(parameter)

    def set_parameter(self,parameter):
        self.parameters = parameter


if __name__ == '__main__':
    parameter = [{
        "url": "http://news.sohu.com/",
        "re_Rule": "http://www.sohu.com/a/\d+_\d+",
        "limit":500
    }]
    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()



