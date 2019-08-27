from utils.spider_utils.xpathtexts import xPathTexts
from utils.base_utils.headers import headers
from urllib.parse import urljoin
from utils.db_utils.mongodbclient import MongodbClient
from utils.base_utils.bloomfilter import filterutil
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
        self.uuid = ''  # id
        self.url = ''  # 网址
        self.title = ''  # 标题
        self.state = ''  # 新旧程度
        self.sale_price = ''  # 售价
        self.discount = ''  # 折扣
        self.price_font = ''  # 原价
        self.brand = ''  # 品牌
        self.type = ''  # 商品类型
        self.human = ''  # 适用人群
        self.addtime = ''  # 采集时间
        self.imgs = ''  # 图片集合

    def __str__(self):
        return "'uuid':'{}','url':'{}','title':'{}'," \
               "'state':'{}','sale_price':'{}','discount':'{}'," \
               "'price_font':'{}','brand':'{}','type':'{}','human':'{}','addtime':'{}','imgs':{}" \
            .format(self.uuid, self.url, self.title,
                    self.state, self.sale_price, self.discount,
                    self.price_font, self.brand, self.type, self.human, self.addtime, self.imgs)


class baseUrl(xPathTexts):
    def __init__(self):
        super(baseUrl, self).__init__()
        self.urls = None
        self.bloomFilter = filterutil("xinshang_data.blm")


    def getUrls(self, url=None, html=None, headers=None):
        X_path = "//ul[@class = 'list']//li//a[1]//@href"
        data = set()
        if html != None:
            self.urls = self.get_contents(X_path=X_path, html=html)
        else:
            self.urls = self.get_contents(url=url, X_path=X_path, headers=headers, cookies=cookies)
        for item in self.urls:
            url = urljoin(url, item)
            if "http" in url:
                filter = self.bloomFilter.filtertext(str(url))
                if filter:
                    data.add(url)
        return data


class parseUrl(baseUrl):
    def __init__(self):
        super(parseUrl, self).__init__()

    def parse(self, html, item):
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
        xsd.url = item
        import datetime
        xsd.addtime = str(datetime.datetime.now())
        try:
            xsd.title = self.get_contents(html=html, X_path=X_title)[0]
        except:
            xsd.title = ""
        try:
            xsd.state = self.get_contents(html=html, X_path=X_state)[1]
        except:
            xsd.state = ""
        try:
            xsd.sale_price = self.get_contents(html=html, X_path=X_sale_price)[0]
        except:
            xsd.sale_price = ""
        try:
            xsd.discount = self.get_contents(html=html, X_path=X_discount)[0]
        except:
            xsd.discount = ""
        try:
            xsd.price_font = self.get_contents(html=html, X_path=X_price_font)[0]
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
        return xsd

    def get_data(self, url=None, headers=None, count=1):
        urls = self.getUrls(url=url, headers=headers)
        temp = urls.copy()
        if len(urls) != 0:
            for item in temp:
                html = self.getHtml(url=item, headers=headers, cookies=cookies)
                yield self.parse(html, item)
        elif len(urls) == 0:
            print("第" + str(count) + "页为空")
            yield count + 1


import json

import threading


class myThread(threading.Thread):
    def __init__(self, sort):
        threading.Thread.__init__(self)
        self.__flag = threading.Event()
        self.momgodb = MongodbClient(
            mongodb_conf={'host': '61.147.124.76', 'port': 27017, 'db_name': 'xs_spider', 'table_name': 'xs_datas'})
        self.sort = sort
        self.baseurl = parseUrl()

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.function(self.sort)

    def function(self, sort):
        i = 1
        count = 1

        while True:
            url = "http://91xinshang.com/{}/n{}/".format(sort, i)
            info = "正在采集" + sort + "模块中的第" + str(i) + "页数据,采集url为" + url
            print(info)
            result = self.baseurl.get_data(url=url, headers=headers, count=count)

            for item in result:
                if isinstance(item, int):
                    if item != 1:
                        count = item
                    if item == 151:
                        print(str(sort)+"模块连续十页为空，重定位为第一页开始采集")
                        count = 1
                        i = 0
                else:
                    item = "{" + str(item) + "}"
                    print(item)
                    self.momgodb.collection.insert(json.loads(str(item).replace("'", '"')))
            i = i + 1

if __name__ == '__main__':

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

