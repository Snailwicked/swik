import requests,time
from utils.headers import random_headers
from lxml import etree
cookies = {
    'acw_tc': '781bad0a15730944068836592e415cdc5b7c4f8bf3d3b354e0485da077703e',
    '_zycg_gov_session': 'BAh7BjoPc2Vzc2lvbl9pZCIlMGNiMTFjZWY1MGQxMmQ2YTFiOGFkYWRjZWQxMWYyODM%3D--67bd357d0584a268b4ce940579d74d8c0f9b8230',
    'UM_distinctid': '16e43bbc4b0175-0d10f41507ce5c-514f291a-1fa400-16e43bbc4b135c',
    'CNZZDATA1000057469': '197821367-1573093506-%7C1573093506',
    'SERVERID': 'cf976378c2a6c465dc783ee421e75bde|1573095881|1573095751',
}

import pymysql

class DbToMysql(object):

    def __init__(self):
        self.con = pymysql.connect(
            host="180.97.15.181",
            user="root",
            password="Vrv123!@#",
            db="zla_db",
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        self.con.close()

    def save_one_data(self,datas):
        sql = "INSERT INTO `purchase` (company_buy,goods,goods_number,price,company_sale,transaction_date,price_sum) " \
              "VALUES ('{0}' ,'{1}', '{2}', '{3}', '{4}',  '{5}', '{6}')".format(str(datas['company_buy']),str(datas['goods']),int(datas['goods_number']),float(datas['price']),str(datas['company_sale']),datas['transaction_date'],int(datas['goods_number'])*float(datas['price']))
        try:
            with self.con.cursor() as cursor:
                cursor.execute(sql)
                self.con.commit()
        except Exception as e:
            return -1
        # finally:
        #     self.close()

dbsql = DbToMysql()


for page in range(1970,2000):
    params = (
        ('page', '{}'.format(page)),
    )
    import random
    time.sleep(random.randint(1,4))
    response = requests.get('http://www.zycg.gov.cn/rjcg/pur_record', headers=random_headers, params=params, cookies=cookies, verify=False)
    print(response.url)
    html_tree = etree.HTML(response.text)
    company_buys = html_tree.xpath("//div[@class= 'tab_box']//table[@class= 'list']//tbody//tr//td[2]//text()")
    company_buys_news = []
    for item in company_buys:
        item = item.replace("\\r",'').replace("\\n",'').replace("\\t","").strip()
        if item != "":
            company_buys_news.append(item)

    goods = html_tree.xpath("//div[@class= 'tab_box']//table[@class= 'list']//tbody//tr//td[3]//a//text()")
    goods = [item.replace("\xa0",' ') for item in goods]

    goods_number = html_tree.xpath("//div[@class= 'tab_box']//table[@class= 'list']//tbody//tr//td[4]//text()")

    price = html_tree.xpath("//div[@class= 'tab_box']//table[@class= 'list']//tbody//tr//td[5]//text()")
    price = [item.replace(",",'') for item in price]

    company_sale = html_tree.xpath("//div[@class= 'tab_box']//table[@class= 'list']//tbody//tr//td[6]//text()")

    t_times = html_tree.xpath("//div[@class= 'tab_box']//table[@class= 'list']//tbody//tr//td[7]//text()")
    import time
    from dateutil.parser import parse as date_parser
    if len(company_buys_news)!=len(goods_number):
        print("企业未买商品",response.url)
        continue
    else:
        for i in range(len(company_buys_news)):
            data = {}
            data["company_buy"] = company_buys_news[i]
            data["goods"] = goods[i]
            data["goods_number"] = goods_number[i]
            data["price"] = price[i]
            data["company_sale"] = company_sale[i]
            timeArray = time.localtime(int(time.mktime(
                date_parser(t_times[i]).timetuple())))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            data["transaction_date"] = otherStyleTime
            dbsql.save_one_data(data)
