# -*- coding: utf-8 -*-
from master.MainURLUtil import MainURLUtil
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.UrlUtils import UrlUtils
from SQL_DB.db.redisclient import RedisClient
import logging.config
from SQL_DB.config.config import Config
# from BloomFilter import filterURL

logger_conf = Config().get_logger_args()
logging.config.dictConfig(logger_conf)


def cut(url):
    url = url.replace("//", "/").replace("///", "/").replace("////", "/").replace("/////", "/").replace("//////",
                                                                                                        "/").replace(
        "///////", "/").replace("////////", "/").replace("/////////", "/")
    text = url.split("/")
    return text


class getNewURL(object):
    def __init__(self, url="https://www.qq.com/"):
        self.url = url
        self.server = RedisClient()
        self.redis_key = "request_url"
        self.start_url = "start_url"
        self.error_start = "error_start"

    def getURL(self):
        lx = MainURLUtil(url=self.url)
        urllist = lx.get_href()
        clf = joblib.load('../master/url_SDG.pkl')
        vocabulary = joblib.load('../master/url_Vocabulary.pkl')
        tv = TfidfVectorizer(tokenizer=cut,
                             vocabulary=vocabulary)
        datas = []
        for url in list(urllist):
            uu = UrlUtils(url=url)
            new_url = uu.get_feature()
            datas.append(new_url)
        traindata = tv.fit_transform(datas)
        pred = clf.predict(traindata)
        urls = list(map(lambda x, y: y + "_" + x, urllist, pred))
        datas = []
        for url in urls:
            if "1_" in url:
                datas.append(url[2:])
        return datas

    def start(self):
        try:
            key = 1
            while key:
                if self.server.get_urlSums(self.redis_key) >= 1000:
                    import time
                    time.sleep(600)
                    continue
                urls = []
                url = self.server.get_urlFromhead(self.start_url)
                test = bytes.decode(url[1])
                logging.info("正在解析<{}>".format(test))
                urls.append(test)
                parseurl = []
                try:
                    getURL = getNewURL(url=test)
                    texts = getURL.getURL()
                    for i in texts:
                        if filterURL(i) != "":
                            parseurl.append(i)
                        else:
                            logging.info("该新闻已存在过滤器中")
                except Exception as e:
                    logging.error("解析异常<{0}>，{1}".format(test, e))
                    self.server.add_urls(self.error_start, urls)
                    self.server.add_urls(self.start_url, urls)
                    continue
                self.server.add_urls(self.redis_key, parseurl)
                logging.info("解析出{}条新闻网址，并成功导入redis数据库".format(len(parseurl)))
                self.server.add_urls(self.start_url, urls)
        except:
            self.server.add_urls(self.start_url, urls)


if __name__ == '__main__':

    url = "http://qiubeixian.okcis.cn"
    getURL = getNewURL(url)
    texts = getURL.getURL()
    for i in texts:
        print(i)
    #
    # urls = open("./start_urls", "r", encoding='utf8', errors='ignore')
    # for line in urls:
    #     url = line.replace("\n", "")
    #     print(url)




    getURL = getNewURL()
    getURL.start()



