from master.collectionurl import filterUrls
from slave.extractors import ContentExtractor
from utils.spiderutils.xpathtexts import xPathTexts

xpath = xPathTexts()


class Parse:
    def __init__(self):
        self.master = filterUrls()

    def get_data(self, urls):
        data = []
        for url in self.master.FilterUrls(urls):
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


if __name__ == "__main__":
    urls = ["https://news.sina.com.cn/"]
    parse = Parse()
    result = parse.get_data(urls)
    print(result)



