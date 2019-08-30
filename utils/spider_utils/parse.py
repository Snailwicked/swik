from utils.master import filterUrls
from utils.slave import ContentExtractor
from utils.spider_utils.xpathtexts import xPathTexts
from utils.exception_utils import parse_text
from db import News_data
xpath = xPathTexts()
new_data =News_data()
class Parse:
    def __init__(self):
        self.master = filterUrls()

    @parse_text
    def get_data(self, urls):
        sub_urls = self.master.FilterUrls(urls)
        if sub_urls != []:
            for url in sub_urls:
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
                    item["publishTime"] = ce.get_publishing_date()
                    item["summary"] = ce.get_summary()
                except Exception as e:
                    print(e)
                print(item)
                new_data.insert(item)

        else:
            print("未解析到数据")


if __name__ == "__main__":
    urls = ["http://media.people.com.cn/"]
    parse = Parse()
    parse.get_data(urls)
