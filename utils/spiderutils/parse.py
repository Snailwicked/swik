from master.collectionurl import filterUrls
from slave.extractors import ContentExtractor
from utils.spiderutils.xpathtexts import xPathTexts


class Parse():

    def __init__(self):
        self.master = filterUrls()
        self.xpath = xPathTexts()

    def getData(self,urls):
        for url in self.master.FilterUrls(urls):
            try:
                html = self.xpath.getHtml(url)
                ce = ContentExtractor(html=html,url=url)
                print(url,ce.get_title())
            except:
                pass
        return True

if __name__ == "__main__":
    urls = ["https://news.sina.com.cn/"]
    parse = Parse()
    result = parse.getData(urls)
    print(result)