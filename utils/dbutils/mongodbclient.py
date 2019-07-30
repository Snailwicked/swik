# -*- coding: utf-8 -*-
"""
    说明 ：针对mongodb数据库的各种操作
    参数 ：无
    类型 ：无
    作者 ：王明辉
    创建时间 ：2018-8-14 19.09
"""
from pymongo import MongoClient
import json


class MongodbClient(object):
    def __init__(self,mongodb_conf =None):
        # mongodb_conf={'host': '101.132.113.50', 'port': 27017, 'db_name': 'spider', 'table_name': 'test'}
        self.mongodb_conf = mongodb_conf
        self.client = MongoClient(host=self.mongodb_conf['host'], port=self.mongodb_conf['port'])
        self.db = self.client[self.mongodb_conf['db_name']]
        self.collection = self.db[self.mongodb_conf['table_name']]

    """ 
        名称 ：查询mongodb数据库数据
        说明 ：查询所有可访问且re_url不为空的网站
        参数 ：无
        类型 ：无
        返回值类型 ：list
        作者 ：王明辉
        创建时间 ：2018-8-14 19.09
    """


if __name__ == "__main__":
    db = MongodbClient(mongodb_conf ={'host': '101.132.113.50', 'port': 27017, 'db_name': 'spider_manage', 'table_name': 'config'})
    import uuid

    # data = {'uuid':'8ca3784a-5a71-11e9-b147-005056c00008','url':'http://91xinshang.com/xianzhi/U0RjNXY2Um9aZ1k9.html','title':'Tiffany & Co. 蒂芙尼罗马数字项圈项链','state':'9成新','sale_price':'997','discount':'2折','price_font':'原价: ¥4999','brand':'Tiffany & Co.','type':'首饰配饰/项链/吊坠','human':'女士','addtime':'','imgs':['http://img.91sph.com/goods//20190330//5d5d86ff3cf647d68ddd0e153796106d_s2.jpg', 'http://img.91sph.com/goods//20190330//7c292e0cc7ee4d57b9edc33fd78dce60_s2.jpg', 'http://img.91sph.com/goods//20190330//f310eef3d8254f24b5caa4ed248a1522_s2.jpg', 'http://img.91sph.com/goods//20190330//f9ef4810d30d4954afc61f889f436321_s2.jpg']}
    # main_url ,re_url= db.select_one_and_delete()
    # print(main_url,re_url)
    # 更新操作
    # for result in db.select_all():
    #     main_url = result.get("main_url")
    #     condition = {'main_url': main_url}
    #     re =str(result.get('re_url')).replace("\\","\\\\")
    #     result['re_url'] =re
    #     db.update_one(condition,result)
    #     print(result)
    # print()
    # db.insert_one(data)
    data = [{"uuid": str(uuid.uuid1()),
     "urls": ["https://news.sina.com.cn/","http://news.sohu.com/","https://news.163.com/"],
    "start_time": "",
    "limit": "1",
    "fixed_time": "10:00",
    "agent":"1"
    },{"uuid": str(uuid.uuid1()),
     "urls": ["http://news.sohu.com/","https://news.163.com/"],
    "start_time": "",
    "limit": "1",
    "fixed_time": "08:00",
    "agent":"1"
    },{"uuid": str(uuid.uuid1()),
     "urls": ["https://news.sina.com.cn/"],
    "start_time": "",
    "limit": "1",
    "fixed_time": "03 10:00",
    "agent":"1"
    }]
    db.insert(data)
    print()
        # re_url =result.get("re_url")
        # re =json.loads(re_url)
        # print(re.get('re0'))

