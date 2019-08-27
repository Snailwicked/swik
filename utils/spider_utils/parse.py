from utils.master import filterUrls
from utils.slave import ContentExtractor
from utils.spider_utils.xpathtexts import xPathTexts
from decorators import parse_text

xpath = xPathTexts()

@parse_text
class Parse:
    def __init__(self):
        self.master = filterUrls()

    def get_data(self, urls):
        data = []
        sub_urls = self.master.FilterUrls(urls)
        if sub_urls != []:
            for url in sub_urls:
                item= {}
                try:
                    xpath.set_parameter(url=url)
                    ce = ContentExtractor(html=xpath.html, url=url)
                    item["url"] = url
                    item["authors"] = ce.get_authors()
                    item["publishing_date"] = ce.get_publishing_date()
                    item["summary"] = ce.get_summary()
                    print(url,item)
                    data.append(item)
                except Exception as e:
                    print(e)
            return data
        else:
            print("未解析到数据")


if __name__ == "__main__":
    urls = ["http://media.people.com.cn/"]
    parse = Parse()
    result = parse.get_data(urls)
    print(result)
