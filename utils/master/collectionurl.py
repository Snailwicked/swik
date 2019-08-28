from utils.spider_utils.xpathtexts import xPathTexts
from urllib.parse import urljoin
from utils.url_utils.transurl import transUrls
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
xpath = xPathTexts()
from config.conf import get_algorithm
args = get_algorithm()


class filterUrl():

    def __init__(self):
        self.clf = joblib.load(args["url_SDG"])
        self.vocabulary = joblib.load(args["url_Vocabulay"])
        self.tv = TfidfVectorizer(tokenizer=self.cut,
                                  vocabulary=self.vocabulary)
        self.transurls = transUrls()

    def cut(self,url):
        url = url.replace("//", "/").replace("///", "/").replace("////", "/").replace("/////", "/").replace("//////","/").replace(
            "///////", "/").replace("////////", "/").replace("/////////", "/")
        text = url.split("/")
        return text

    def getFilterUrls(self,url):
        xpath.set_parameter(url=url)
        data = set()
        for item in xpath.get_contents(X_path="//a//@href"):
            url = urljoin(url, item)
            if "http" in url:
                data.add(url)

        try:
            train = self.transurls.transport(list(data))
            traindata = self.tv.fit_transform(train)
            pred = self.clf.predict(traindata)
            after_urls = list(map(lambda x, y: y + "_" + x, list(data), pred))
            for after in after_urls:
                if "1_" in after:
                    yield after[2:]
        except:
            print("解析不到网址")
            return []
#
class filterUrls(filterUrl):

    def FilterUrls(self,urls):
        if not isinstance(urls, list):
            temp = []
            temp.append(urls)
            for url in temp:
                yield from self.getFilterUrls(url)
        else:
            for url in urls:
                yield from self.getFilterUrls(url)

if __name__ == "__main__":
    url = "http://www.jsjjw.cn/news/page/node_1061.htm"
    mainurl = filterUrls()
    for url in mainurl.FilterUrls(url):
        print(url)
