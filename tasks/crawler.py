from urllib.parse import urljoin
from config import *
import sys
import re
from collections import defaultdict
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import transUrls
from config.conf import get_algorithm
from utils import xPathTexts
from utils.spider_utils import Parse
import time,json
args = get_algorithm()
parse = Parse()
from db.redis_db import Url_Parameter
url_storage = Url_Parameter()


class Crawler:
    def __init__(self):
        self.xpath = xPathTexts()
        self.brief = defaultdict(set)
        self.count = 0
        self.start_time = time.time()


    def run(self,parameter):
        self.parameter = parameter
        self.rule = json.loads(str(self.parameter['rule']))
        self.limit = int(self.rule["deep_limit"]) if self.rule["deep_limit"] !="" else 1
        self.xpath_urls([self.parameter["url"]],0)


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


    def xpath_urls(self, urls,limit):
        if limit == self.limit:
            end_time = time.time()
            crawler_info.info("{} has been collected and program is finished".format(self.parameter["url"]))
            crawler_info.info("{} parsesed {} websites and spending time {}".format(self.parameter["url"],self.count,(end_time-self.start_time)))
            try:
                sys.exit()
            except:
                pass
        else:
            filter_rule =self.rule["filter_rule"]
            if filter_rule:
                target_url = []
                catalogue = []
                for url  in urls:
                    for item in self.get_hrefs(url):
                        result = re.findall(filter_rule, item)
                        if result and  item not in self.brief["target_url"]:
                            target_url.append(item)
                            self.brief["target_url"].add(item)
                        elif item not in self.brief["catalogue"]:
                            catalogue.append(item)
                            self.brief["catalogue"].add(item)
                self.count = self.count+len(target_url)
                [self.process(url) for url in target_url]
                self.xpath_urls(catalogue,limit+1)
            else:
                self.clf = joblib.load(args["url_SDG"])
                self.vocabulary = joblib.load(args["url_Vocabulay"])
                self.tv = TfidfVectorizer(tokenizer=self.cut, vocabulary=self.vocabulary)
                self.transurls = transUrls()
                target_url = []
                catalogue = []
                for url in urls:
                    urls = self.get_hrefs(url)
                    train = self.transurls.transport(list(urls))
                    try:
                        traindata = self.tv.fit_transform(train)
                    except:
                        crawler_info.error("{} cannot be parsed by algorithms".format(url))
                        continue
                    pred = self.clf.predict(traindata)
                    after_urls = list(map(lambda x, y: y + "_" + x, list(urls), pred))
                    for after in after_urls:
                        if "1_" in after and after not in self.brief["target_url"]:
                            target_url.append(after[2:])
                            self.brief["target_url"].add(after[2:])
                        elif after not in self.brief["catalogue"]:
                            catalogue.append(after[2:])
                            self.brief["catalogue"].add(after[2:])
                [self.process(url) for url in target_url]
                self.count = self.count+len(target_url)
                self.xpath_urls(catalogue,limit+1)

    def process(self, url):
        # parse.get_data(target_url)
        parameter = {}
        parameter["url"] = url
        url_storage.store_parameter("新闻爬虫",parameter)


class Crawleruning(Crawler):

    def __init__(self):
        super(Crawleruning, self).__init__()

    def start(self):
        crawler_info.info(self.parameters)
        self.run(self.parameters)
    def set_parameter(self,parameter):
        self.parameters = parameter


if __name__ == '__main__':
    parameter = {
        "url": "http://www.cyol.com/",
        "rule": {'author': '', 'filter_rule': '', 'page_size': '1', 'content': '', 'header': '', 'issueTime': ''},
    }
    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()


    # from celery.task.control import revoke
    #
    # revoke("de8d5e67-33b6-4980-8846-54e24551dda6", terminate=True)
