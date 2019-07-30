from utils.spiderutils.xpathtexts import xPathTexts
from urllib.parse import urljoin
from utils.urlutils.transurl import transUrls
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
xpath = xPathTexts()


class filterUrl():

    def __init__(self):
        self.clf = joblib.load('E:/Workspace/swik/algorithm/pkl/url_SDG.pkl')
        self.vocabulary = joblib.load('E:/Workspace/swik/algorithm/pkl/url_Vocabulary.pkl')
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


        train = self.transurls.transport(list(data))
        traindata = self.tv.fit_transform(train)
        pred = self.clf.predict(traindata)
        after_urls = list(map(lambda x, y: y + "_" + x, list(data), pred))
        for after in after_urls:
            if "1_" in after:
                yield after[2:]
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
