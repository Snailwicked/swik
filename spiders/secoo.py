import requests
from utils.spiderutils.xpathtexts import xPathTexts
from utils.baseutils.headers import headers
import time
from utils.baseutils.bloomfilter import filterutil
from urllib.parse import urljoin

page = 2


def fetch(sub ,this_page_time,pre_page_time):
    if sub == 1:
        return  {
            '_ga': 'GA1.2.831389087.1557454263',
            'gr_user_id': '263b75c1-0681-41e9-b97a-fa70240f95cd',
            '__utmz': '145630134.1557454263.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'grwng_uid': '8a1f2fd1-d154-4daa-86e6-80e82ecc504f',
            'NTKF_T2D_CLIENTID': 'guestB03968D9-BCD8-914D-391B-9F821447E4D1',
            '__jsluid': '2053ee98553553c408933b598f6a624c',
            'Hm_lvt_b844e792cd7084d8aae7a1d885ef5c29': '1557454263,1557473474',
            '__utmc': '145630134',
            '_jzqc': '1',
            '_jzqckmp': '1',
            'nTalk_CACHE_DATA': '{uid:ck_1000_ISME9754_guestB03968D9-BCD8-91,tid:1557710887107919}',
            '_gid': 'GA1.2.1276657075.1557711079',
            '_qzjc': '1',
            'BIGipServerpool_proxy': '1043507392.20480.0000',
            'ab95574fe95f2817_gr_session_id': 'fdc3c2bf-39e6-4c49-9d39-0ff05ad97b6e',
            'ab95574fe95f2817_gr_session_id_fdc3c2bf-39e6-4c49-9d39-0ff05ad97b6e': 'true',
            '__utma': '145630134.831389087.1557454263.1557710887.1557715461.4',
            '_jzqa': '1.436690445282648260.1557454269.1557710887.1557715461.4',
            '_jzqx': '1.1557715461.1557715461.1.jzqsr=list%2Esecoo%2Ecom|jzqct=/bags/30-0-0-0-0-1-0-0-1-10-0-0%2Eshtml.-',
            '__utmt_UA-40733470-5': '1',
            'search_req_id': '2da367cc-e4f0-4d04-a404-fdd6f30e09a4',
            '__xsptplusUT_219': '1',
            'Hm_lpvt_b844e792cd7084d8aae7a1d885ef5c29': str(round(this_page_time/1000)),
            '_dc_gtm_UA-40733470-1': '1',
            '__utmb': '145630134.10.10.1557715461',
            '_jzqb': '1.6.10.1557715461.1',
            '__xsptplus219': '219.4.1557715461.1557716701.5%234%7C%7C%7C%7C%7C%23%23WMixaKR84Fq2omJB-EeCa03zCg8qoEb9%23',
            '_qzja': '1.2060655711.1557454268682.1557711095162.1557715461404.{0}.{1}.0.0.0.20.3'.format(str(pre_page_time),str(this_page_time)),
            '_qzjb': '1.1557715461404.4.0.0.0',
            '_qzjto': '8.2.0',
            'ST_FPC': 'id=2da4b33c1252a8af5de1557454263665:lv=1557716702224:ss=1557715453522:lsv=1557710890707:vs=4:spv=5',}

    cookies = {
        '_ga': 'GA1.2.831389087.1557454263',
        'gr_user_id': '263b75c1-0681-41e9-b97a-fa70240f95cd',
        '__utmz': '145630134.1557454263.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'grwng_uid': '8a1f2fd1-d154-4daa-86e6-80e82ecc504f',
        'NTKF_T2D_CLIENTID': 'guestB03968D9-BCD8-914D-391B-9F821447E4D1',
        '__jsluid': '07f1deb196113725227ea1009489e227',
        'Hm_lvt_b844e792cd7084d8aae7a1d885ef5c29': '1557454263,1557473474',
        '__utmc': '145630134',
        '_jzqc': '1',
        '_jzqckmp': '1',
        '_gid': 'GA1.3.1802212844.1557710887',
        '_jzqx': '1.1557715461.1557715461.1.jzqsr=list%2Esecoo%2Ecom|jzqct=/bags/30-0-0-0-0-1-0-0-1-10-0-0%2Eshtml.-',
        'ab95574fe95f2817_gr_session_id': '5add844f-97a0-4b0d-9733-5a3c201e14e8',
        'ab95574fe95f2817_gr_session_id_5add844f-97a0-4b0d-9733-5a3c201e14e8': 'true',
        '__utma': '145630134.831389087.1557454263.1557715461.1557727856.5',
        '__utmt_UA-40733470-5': '1',
        '_jzqa': '1.436690445282648260.1557454269.1557715461.1557727856.5',
        'nTalk_CACHE_DATA': '{uid:ck_1000_ISME9754_guestB03968D9-BCD8-91,tid:1557727856355168}',
        'Hm_lpvt_b844e792cd7084d8aae7a1d885ef5c29': str(round(this_page_time/1000)),
        '__utmb': '145630134.6.10.1557727856',
        '_dc_gtm_UA-40733470-1': '1',
        '_qzja': '1.58478894.1557454276353.1557716175725.1557727855938.{0}.{1}.0.0.0.20.5'.format(str(pre_page_time),str(this_page_time)),
        '_qzjb': '1.1557727855938.3.0.0.0',
        '_qzjc': '1',
        '_qzjto': '19.3.0',
        '_jzqb': '1.6.10.1557727856.1',
        '__xsptplus219': '219.5.1557727856.1557728146.3%234%7C%7C%7C%7C%7C%23%23-z8rEz21dJs5hSQephYBvalxtGPN5nYv%23',
        'ST_FPC': 'id=2da4b33c1252a8af5de1557454263665:lv=1557728147504:ss=1557727856496:lsv=1557715453522:vs=5:spv=3',
    }


    return cookies


class seCooData():
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
        self.material = ''#材质
        self.size = ""#大小
        self.colour = "" #颜色
        self.origin = "" #产地

    def __str__(self):
        return "'uuid':'{}','url':'{}','title':'{}'," \
               "'state':'{}','sale_price':'{}','discount':'{}'," \
               "'price_font':'{}','brand':'{}','type':'{}','human':'{}','addtime':'{}','imgs':{},'material':'{}','size':'{}','colour':'{}','origin':'{}'" \
            .format(self.uuid, self.url, self.title,
                    self.state, self.sale_price, self.discount,
                    self.price_font, self.brand, self.type, self.human, self.addtime, self.imgs,self.material,self.size,self.colour,self.origin)


class baseUrl(xPathTexts):
    def __init__(self):
        super(baseUrl, self).__init__()
        self.urls = None
        self.bloomFilter = filterutil("secoo_data.blm")


    def getUrls(self, url=None, html=None, headers=None):
        X_path = "//dd[@class = 'dl_name']//a//@href"
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

    def parse(self, html, item,sort):
        scd = seCooData()
        X_title = "//div[@class = 'proName']//h2//text()"
        X_price = "//strong[@id = 'secooPriceJs']//text()"
        X_human = "//div[@class = 'zxx_con']//text()"
        X_imgs = "//div[@class = 'move_box']//div//a//@bigsrc"
        X_param = self.get_contents(html=response.text, X_path=X_human)

        scd.uuid = str(uuid.uuid1())
        import datetime
        scd.url = item

        scd.addtime = str(datetime.datetime.now())
        scd.state = "全新"
        scd.discount = ""
        scd.type = sort
        try:
            scd.title = self.get_contents(html=html, X_path=X_title)[0]
        except:
            scd.title = ""
        try:
            scd.sale_price =  self.get_contents(html=html, X_path=X_price)[0]
            scd.price_font =  self.get_contents(html=html, X_path=X_price)[0]
        except:
            scd.sale_price = ""
            scd.price_font = ""
        try:
            scd.brand = X_param[-2:-1][0]
        except:
            scd.brand = ""
        try:
            scd.imgs = self.get_contents(html=html, X_path=X_imgs)
        except:
            scd.imgs = []

        try:
            for item in X_param[:-3]:
                temp = item.split("：")
                if temp[0]=="适用人群":
                    scd.human = temp[1]
                if temp[0]=="材质":
                    scd.material = temp[1]
                if temp[0]=="尺寸":
                    scd.size = temp[1]
                if temp[0]=="颜色":
                    scd.colour = temp[1]
                if temp[0]=="产地":
                    scd.origin = temp[1]
        except:
            scd.human = ""
            scd.material = ""
            scd.size = ""
            scd.colour = ""
            scd.origin = ""
        return scd
from dbs.mongodbclient import MongodbClient

momgodb = MongodbClient(
            mongodb_conf={'host': '192.168.30.66', 'port': 27017, 'db_name': 'xs_spider', 'table_name': 'seco_datas'})
bloomFilter = filterutil("secoo_data.blm")
pre_page_time = int(round(time.time() * 1000))
for item in range(1,1000):

    this_page_time = int(round(time.time() * 1000))
    cookies = fetch(1,this_page_time,pre_page_time)
    pre_page_time = this_page_time
    response = requests.get('http://list.secoo.com/bags/30-0-0-0-0-1-0-0-{}-10-0-0-100-0.shtml'.format(item), headers=headers, cookies=cookies)
    import time
    import random

    pause_time = random.randint(1, 4)
    time.sleep(pause_time)
    X_path = "//dd[@class = 'dl_name']//a//@href"
    xpt = xPathTexts()
    urls = xpt.get_contents(html=response.text,X_path=X_path)
    print("正在采集第"+str(item)+"页信息")
    for url in urls:
        filter = bloomFilter.filtertext(str(url))
        if filter:
            scd = seCooData()
            this_page_time = int(round(time.time() * 1000))
            cookies = fetch(0, this_page_time, pre_page_time)
            pre_page_time = this_page_time
            pause_time = random.randint(1, 4)
            time.sleep(pause_time)
            response = requests.get(url,
                                    headers=headers, cookies=cookies)

            html = response.text


            X_title = "//div[@class = 'proName']//h2//text()"
            X_price = "//strong[@id = 'secooPriceJs']//text()"
            X_human = "//div[@class = 'zxx_con']//text()"
            X_imgs = "//div[@class = 'move_box']//div//a//@bigsrc"

            xpt = xPathTexts()
            X_param = xpt.get_contents(html=response.text, X_path=X_human)

            import uuid

            scd.uuid = str(uuid.uuid1())
            scd.url = url
            import datetime

            scd.addtime = str(datetime.datetime.now())
            scd.state = "全新"
            scd.discount = ""
            scd.type = "包袋"
            try:
                scd.title = str(xpt.get_contents(html=response.text, X_path=X_title)[0]).replace("\"","").replace("'","")
            except:
                scd.title = ""
            try:
                scd.sale_price =  xpt.get_contents(html=response.text, X_path=X_price)[0]
                scd.price_font =  xpt.get_contents(html=response.text, X_path=X_price)[0]
            except:
                scd.sale_price = ""
                scd.price_font = ""
            try:
                scd.brand = X_param[-2:-1][0]
            except:
                scd.brand = ""
            try:
                scd.imgs = xpt.get_contents(html=response.text, X_path=X_imgs)
            except:
                scd.imgs = []

            try:
                for item in X_param[:-3]:
                    temp = item.split("：")
                    if temp[0]=="适用人群":
                        scd.human = temp[1]
                    if temp[0]=="材质":
                        scd.material = temp[1]
                    if temp[0]=="尺寸":
                        scd.size = str(temp[1]).replace("\"","").replace("'","")
                    if temp[0]=="颜色":
                        scd.colour = temp[1]
                    if temp[0]=="产地":
                        scd.origin = temp[1]
            except:
                scd.human = ""
                scd.material = ""
                scd.size = ""
                scd.colour = ""
                scd.origin = ""

            item = "{" + str(scd.__str__()) + "}"
            import json
            print(scd.__str__())
            momgodb.insert(json.loads(str(item).replace("'", '"')))
