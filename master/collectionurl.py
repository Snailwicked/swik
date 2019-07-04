from utils.spiderutils.xpathtexts import xPathTexts
from utils.baseutils.headers import headers
from urllib.parse import urljoin
from utils.urlutils.transurl import transUrls
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


class baseUrl(xPathTexts):
    def __init__(self):
        super(baseUrl, self).__init__()
        self.urls = None

    def getUrls(self,url =None,html = None,header=None):
        X_path = "//a//@href"
        data = set()
        if html!= None:
            self.urls = self.get_contents(X_path=X_path, html=html, headers=header)
        else:
            self.urls = self.get_contents(url=url, X_path=X_path, headers=header)
        for item in self.urls:
            url = urljoin(url, item)
            if "http" in url:
                data.add(url)
        return list(data)

class filterUrl(baseUrl):
    def __init__(self):
        super(baseUrl, self).__init__()
        self.clf = joblib.load('../algorithm/pkl/url_SDG.pkl')
        self.vocabulary = joblib.load('../algorithm/pkl/url_Vocabulary.pkl')
        self.tv = TfidfVectorizer(tokenizer=self.cut,
                                  vocabulary=self.vocabulary)
        self.transurls = transUrls()

    def cut(self,url):
        url = url.replace("//", "/").replace("///", "/").replace("////", "/").replace("/////", "/").replace("//////","/").replace(
            "///////", "/").replace("////////", "/").replace("/////////", "/")
        text = url.split("/")
        return text

    def getFilterUrls(self,url):
        data = self.getUrls(url)
        train = self.transurls.transport(data)
        traindata = self.tv.fit_transform(train)
        pred = self.clf.predict(traindata)
        after_urls = list(map(lambda x, y: y + "_" + x, list(data), pred))
        for after in after_urls:
            if "1_" in after:
                yield after[2:]

class filterUrls(filterUrl):

    def FilterUrls(self,urls):
        for url in urls:
            yield from self.getFilterUrls(url)
if __name__ == "__main__":
    url = ["http://www.jsjjw.cn/news/page/node_1061.htm"]
    mainurl = filterUrls()
    for url in mainurl.FilterUrls(url):
        print(url)
