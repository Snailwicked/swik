from urllib.parse import urljoin
import re
from collections import defaultdict
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import transUrls
from config.conf import get_algorithm
from utils import xPathTexts
args = get_algorithm()


class Crawler:
    def __init__(self):
        self.dataset = set()
        self.xpath = xPathTexts()
        self.brief = defaultdict(set)
        self.count = 0
        self.sit = 0

    def run(self,parameter):
       self.parameter = parameter
       self.point = 0
       self.xpath_urls([(self.parameter["url"],self.point)])


    def cut(self,url):
        url = url.replace("//", "/").replace("///", "/").replace("////", "/").replace("/////", "/").replace("//////","/").replace(
            "///////", "/").replace("////////", "/").replace("/////////", "/")
        text = url.split("/")
        return text

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
        try:
            filter_rule = self.parameter['rule']["filter_rule"]
        except:
            filter_rule = None
        if filter_rule:
            for url ,point in urls:
                self.point = point
                if point == int(self.parameter['rule']["page_size"]):
                    break
                TEMP = set()
                for item in self.get_hrefs(url):
                    result = re.findall(self.parameter['rule']["filter_rule"], item)
                    if result and item not in self.brief["parsing"]:
                        print(item)
                        self.brief["parsing"].add(item)
                    else:
                        if item not in self.brief["crawled"]:
                            self.brief["crawled"].add(item)
                            TEMP.add(item)
                self.xpath_urls([(item ,self.point+1)for item in TEMP])
        else:

            self.clf = joblib.load(args["url_SDG"])
            self.vocabulary = joblib.load(args["url_Vocabulay"])
            self.tv = TfidfVectorizer(tokenizer=self.cut,
                                      vocabulary=self.vocabulary)
            self.transurls = transUrls()
            result = []

            for url, point in urls:
                urls = self.get_hrefs(url)
                train = self.transurls.transport(list(urls))
                try:
                    traindata = self.tv.fit_transform(train)
                except:
                    return result
                pred = self.clf.predict(traindata)
                after_urls = list(map(lambda x, y: y + "_" + x, list(urls), pred))
                result = []
                for after in after_urls:
                    if "1_" in after:
                        print(after[2:])
                        result.append(after[2:])
                return result
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
        "url": "http://www.sohu.com/",
        "rule": {'author': '', 'filter_rule': '', 'page_size': '1', 'content': '', 'header': '', 'issueTime': ''},
    }]
    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()



