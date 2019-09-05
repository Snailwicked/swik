from urllib.parse import urljoin
from db.dao import MainUrlOper
from config import *
import sys
import re
from collections import defaultdict
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import transUrls
from config.conf import get_algorithm
from utils import xPathTexts
import time,json
args = get_algorithm()
from db.redis_db import Url_Parameter
url_storage = Url_Parameter()
main_url_oper = MainUrlOper()


class Crawler:
    def __init__(self):
        self.xpath = xPathTexts()
        self.brief = defaultdict(set)
        self.count = 0
        self.start_time = time.time()
        self.end_time = None

        self.target_urls = []


    def run(self,parameter):
        self.parameter = parameter
        self.rule = self.parameter['rule']
        self.limit = int(self.rule["deep_limit"]) if self.rule["deep_limit"] !="" else 1
        self.xpath_urls([self.parameter["url"]],0)


    def cut(self,url):
        text = url.split("/")
        return  [element for element in text if element != ""]

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
            self.end_time = time.time()
            crawler_info.info("{} has been collected and program is finished".format(self.parameter["url"]))
            crawler_info.info("{} parsesed {} websites and spending time {}".format(self.parameter["url"],self.count,(self.end_time-self.start_time)))
            if self.count<20:
                pid = self.parameter['pid']
                parameter = {}
                parameter["pid"] = pid
                parameter["status"] = 0
                parameter["spider_name"] = 0

                main_url_oper.update_mainurl(parameter)
                crawler_info.info("Exceptions may occur if the number of {} is too small".format(self.parameter["url"]))
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
                self.target_urls.extend(target_url)
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
                self.target_urls.extend(target_url)
                self.count = self.count+len(target_url)
                self.xpath_urls(catalogue,limit+1)

    def process(self):
        return self.target_urls

    def monitor_info(self):
        self.end_time = time.time()
        return {"url":self.parameter["url"],"count":self.count,"spending_time":self.end_time - self.start_time}



class Crawleruning(Crawler):

    def __init__(self):
        super(Crawleruning, self).__init__()

    def start(self):
        self.run(self.parameters)

    def set_parameter(self,parameter):
        self.parameters = parameter


if __name__ == '__main__':
    parameter = {'url': 'http://www.legalweekly.cn/', 'rule': {'filter_rule': 'https://www.legalweekly.cn/\\w+/\\d+.html', 'selector': 'xpath选择器', 'deep_limit': 1, 'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}}
    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()


    # from celery.task.control import revoke
    #
    # revoke("de8d5e67-33b6-4980-8846-54e24551dda6", terminate=True)
