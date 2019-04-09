from utils.spiderutils.xpathtexts import xPathTexts
from utils.baseutils.headers import headers
from urllib.parse import urljoin
from dbs.mongodbclient import MongodbClient
import asyncio

import uuid
import time

cookies = {
    'JSESSIONID': 'abcBS5CeP0ZaRcdC1BhNw',
    '_uuid': 'CF6436544EF002D5277169C76F573DB8',
    '_ga': 'GA1.2.834059056.1553829157',
    '_gid': 'GA1.2.2103512660.1553829157',
    'Hm_lvt_0ad737e4b4ab167a30f27d43256ff3c8': '1553829157',
    'sajssdk_2015_cross_new_user': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22169c76f59055d6-009f4b14f4d9a1-5a40201d-2073600-169c76f5906543%22%2C%22%24device_id%22%3A%22169c76f59055d6-009f4b14f4d9a1-5a40201d-2073600-169c76f5906543%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
    'downloadLayerState': '1',
    'showLoginPop': '1',
    'Hm_lpvt_0ad737e4b4ab167a30f27d43256ff3c8': str(int(time.time()))}

class xinShangData():
    def __init__(self):
        self.uuid = ''        #id
        self.url = ''         #网址
        self.title = ''       #标题
        self.state = ''       #新旧程度
        self.sale_price = ''  #售价
        self.discount = ''    #折扣
        self.price_font = ''  #原价
        self.brand = ''       #品牌
        self.type = ''        #商品类型
        self.human = ''       #适用人群
        self.addtime = ''     #采集时间
        self.imgs = ''        #图片集合

    def __str__(self):
        return "'uuid':'{}','url':'{}','title':'{}'," \
               "'state':'{}','sale_price':'{}','discount':'{}'," \
               "'price_font':'{}','brand':'{}','type':'{}','human':'{}','addtime':'{}','imgs':{}" \
            .format(self.uuid,self.url, self.title,
                    self.state, self.sale_price,self.discount,
                    self.price_font,self.brand, self.type,self.human,self.addtime,self.imgs)

class baseUrl(xPathTexts):
    def __init__(self):
        super(baseUrl, self).__init__()
        self.urls = None

    def getUrls(self,url =None,html = None,headers=None):
        X_path = "//ul[@class = 'list']//li//a[1]//@href"
        data =set()
        if html!= None:
            self.urls = self.get_contents(X_path=X_path, html=html)
        else:
            self.urls = self.get_contents(url=url, X_path=X_path, headers=headers,cookies=cookies)
        for item in self.urls:
            url = urljoin(url, item)
            if "http" in url:
                data.add(url)
        return data

class parseUrl(baseUrl):
    def __init__(self):
        super(parseUrl, self).__init__()
    def get_data(self,url=None,headers=None):
        for itme in  self.getUrls(url=url,headers=headers):
            html = self.getHtml(url=itme,headers=headers,cookies=cookies)
            xsd = xinShangData()
            X_title = "//h3[@class = 'goods-name']//text()"
            X_sale_price = "//span[@class = 'sale-price']//b//text()"
            X_discount = "//em[@class = 'discount']//text()"
            X_price_font = "//span[@class = 'price-font']//text()"
            X_brand = "//article[@class = 'argument']//p[1]//a//text()"
            X_state = "//article[@class = 'argument']//p[2]//text()"
            X_type = "//article[@class = 'argument']//p[3]//a//text()"
            X_human = "//article[@class = 'argument']//p[4]//text()"
            X_imgs = "//div[@class = 'details-middle-img']//img//@src"
            xsd.uuid = str(uuid.uuid1())
            xsd.url=itme
            import datetime
            xsd.addtime = str(datetime.datetime.now())
            try:
                xsd.title = self.get_contents(html=html, X_path=X_title)[0]
            except:
                xsd.title = ""
            try:
                xsd.state = self.get_contents(html=html, X_path=X_state)[1]
            except:
                xsd.state= ""
            try:
                xsd.sale_price = self.get_contents(html=html,X_path=X_sale_price)[0]
            except:
                xsd.sale_price = ""
            try:
                xsd.discount = self.get_contents(html=html,X_path=X_discount)[0]
            except:
                xsd.discount = ""
            try:
                xsd.price_font = self.get_contents(html=html,X_path=X_price_font)[0]
            except:
                xsd.price_font = ""
            try:
                xsd.brand = self.get_contents(html=html, X_path=X_brand)[0]
            except:
                xsd.brand = ""
            try:
                xsd.type = self.get_contents(html=html, X_path=X_type)[0]
            except:
                xsd.type = ""
            try:
                xsd.human = self.get_contents(html=html, X_path=X_human)[1]
            except:
                xsd.human = ""
            try:
                xsd.imgs = self.get_contents(html=html, X_path=X_imgs)
            except:
                xsd.imgs = []
            yield xsd


import json


def function(sort):
    for i in range(1, 100):
        url = "http://91xinshang.com/{}/n{}/".format(sort, i)
        baseurl = parseUrl()
        for item in baseurl.get_data(url=url, headers=headers):
            print(item)

import threading


class myThread(threading.Thread):
    def __init__(self, sort):
        threading.Thread.__init__(self)
        self.momgodb = MongodbClient(mongodb_conf ={'host': '192.168.30.66', 'port': 27017, 'db_name': 'xs_spider', 'table_name': 'xs_data'})
        self.sort = sort

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.function(self.sort)

    def function(self,sort):
        for i in range(1, 10):
            url = "http://91xinshang.com/{}/n{}/".format(sort, i)
            baseurl = parseUrl()
            for item in baseurl.get_data(url=url, headers=headers):
                item= "{" + str(item) + "}"
                print(item)
                self.momgodb.insert_one(json.loads(str(item).replace("'",'"')))
        self.momgodb.close()


# 创建新线程


if __name__ == '__main__':
    classification = ["bag","shoes","watch","yifu","shoushi"]

    thread1 = myThread("bag")
    thread2 = myThread("shoes")
    thread3 = myThread("yifu")
    thread4 = myThread("watch")
    thread5 = myThread("shoushi")


    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()