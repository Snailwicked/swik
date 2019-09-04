from utils.slave import ContentExtractor
from utils.spider_utils.xpathtexts import xPathTexts
from utils.exception_utils import parse_text
from db import News_data
from config import *

xpath = xPathTexts()
new_data =News_data()
class Parse:


    def __int__(self):
        self.urls = None
    @parse_text
    def get_data(self, urls):
        if not isinstance(urls, list):
            temp = []
            temp.append(urls)
            self.urls = temp
        else:
            self.urls =  urls

        for url in self.urls:
            item= {}
            try:
                xpath.set_parameter(url=url)
                if xpath.html == None:
                    continue
                ce = ContentExtractor(html=xpath.html, url=url)
                item["url"] = url
                item["title"] = ce.get_title()
                item["content"] = ce.get_content()
                item["authors"] = ce.get_authors()
                item["collection_time"] = int(ce.get_thirteenTime())
                item["publish_time"] = int(ce.get_publishing_date())
                item["summary"] = ce.get_summary()
                item["source"] = "中国安全生产网"

            except Exception as e:
                print(e)
                continue
            print(item)
            # crawler_info.info(item)
            new_data.insert(item)



if __name__ == "__main__":
    for i in range(20):

        urls = ["http://www.aqsc.cn/qiye/201905/08/c105573.html"]
        parse = Parse()
        parse.get_data(urls)
