from utils.spiderutils.xpathtexts import xPathTexts
from utils.baseutils.headers import headers
from urllib.parse import urljoin

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
            data = []
            X_title = "//h3[@class = 'goods-name']//text()"
            X_sale_price = "//span[@class = 'sale-price']//b//text()"
            X_discount = "//em[@class = 'discount']//text()"
            X_price_font = "//span[@class = 'price-font']//text()"
            X_brand = "//article[@class = 'argument']//p[1]//a//text()"
            X_state = "//article[@class = 'argument']//p[2]//text()"
            X_type = "//article[@class = 'argument']//p[3]//a//text()"
            X_human = "//article[@class = 'argument']//p[4]//text()"
            X_imgs = "//div[@class = 'details-middle-img']//img//@src"

            title = self.get_contents(html=html,X_path=X_title)
            state = self.get_contents(html=html,X_path=X_state)
            sale_price = self.get_contents(html=html,X_path=X_sale_price)
            discount = self.get_contents(html=html,X_path=X_discount)
            price_font = self.get_contents(html=html,X_path=X_price_font)
            brand = self.get_contents(html=html,X_path=X_brand)
            type = self.get_contents(html=html,X_path=X_type)
            human = self.get_contents(html=html,X_path=X_human)
            imgs= self.get_contents(html=html,X_path=X_imgs)
            data.append(itme)
            data.append(title[0])
            data.append(state[1])
            data.append(sale_price[0])
            try:
                data.append(price_font[0])
            except:
                data.append("")
            try:
                data.append(discount[0])
            except:
                data.append("")
            try:
                data.append(type[0])
            except:
                data.append("")
            try:
                data.append(brand[0])
            except:
                data.append("")
            data.append(human[1])
            data.append(imgs)
            yield data

if __name__ == '__main__':
    classification = ["bag","shoes","watch","yifu","shoushi"]
    for i in range(1,100):
        url = "http://91xinshang.com/bag/n{}/".format(i)
        baseurl = parseUrl()
        for item in  baseurl.get_data(url=url,headers=headers):
            print(item)

