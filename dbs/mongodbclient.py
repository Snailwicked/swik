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
    def __init__(self):
        self.mongodb_conf = {'host': '101.132.113.50', 'port': 27017, 'db_name': 'spider', 'table_name': 'test'}
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
    def select_all(self):
        return self.collection.find()


    def insert_one(self ,jsondata):
        self.collection.insert(jsondata)

    """ 
               名称 ：对mongodb进行查询操作
               参数 ：无
               说明 ：查询任务中的需要采集的网址和新闻正则匹配表达式
               返回值类型 ：string
               作者 ：王明辉
               创建时间 ：2018-8-24 14.16
        """
    def select_one_and_delete(self):
        result= self.collection.find_one_and_delete({})
        main_url = result.get("main_url")
        re_json = result.get("re_url")
        re = json.loads(re_json)
        re_url =re.get('re0')

        return main_url ,re_url



    def delete_one(self):
        pass


    def delete_all(self):
        self.collection.drop()

    """ 
           名称 ：对mongodb进行更新操作
           参数 ：condition ，newdata
           说明 ：condition ={'main_url':'http://ti.zangdiyg.com/'}定位到需要更新的的数据 
                  newdata 对原先的数据进行更改后的数据 newdata =olddata["main_url"] = "http://www.baidu.com"
           类型 ：json
           返回值类型 ：
           作者 ：王明辉
           创建时间 ：2018-8-21 14.16
    """
    def update_one(self,condition ,newdata):
        return self.collection.update_one(condition, {'$set': newdata})

    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.collection:
            self.collection.close()
        return True

if __name__ == "__main__":
    db = MongodbClient()
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
    for result in db.select_all():
        print(result)
        # re_url =result.get("re_url")
        # re =json.loads(re_url)
        # print(re.get('re0'))

