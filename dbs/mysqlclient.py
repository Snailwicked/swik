# -*- coding: utf-8 -*-
import pymysql

'''
mysql 客户端封装接口
用法：
    conf = {'host': '182.254.198.218', 'port': 3306, 'user': 'root', 'password': 'vrv123123',
                           'db_name': 'crawler',
                           'db_table': 'information'}
    mysqlclient = mysqlClient(conf)
    sql =  'insert into information (url,author,title,postTime) values (%s,%s,%s,%s)'
    data = ('http://www.sohu.com/a/304312045_123753', '中国新闻网', '美军证实印度导弹命中卫星 莫迪：具历史性意义', '2019-03-28 09:32:14')
    mysqlclient.insert(sql,data)
    mysqlclient.close()
'''
class mysqlClient():
    def __init__(self,conf = None):
        self.mysql_conf = conf
        self.conn = pymysql.connect(host=self.mysql_conf['host'], port=self.mysql_conf['port'],
                                    user=self.mysql_conf['user'], passwd=self.mysql_conf['password'],
                                    db=self.mysql_conf['db_name'], charset="utf8")

    def insert_data(self, sql,data):
        '''
        :param sql: 'insert into information (url,author,title,postTime) values (%s,%s,%s,%s)'
        :param data: ('http://www.sohu.com/a/304312045_123753', '中国新闻网', '美军证实印度导弹命中卫星 莫迪：具历史性意义', '2019-03-28 09:32:14')
        :return:
        '''
        try:
            self.cursor.execute(sql,data)
            print("数据添加成功")
            self.conn.commit()
        except:
            print("数据添加异常")
            self.conn.rollback()

    def select_all(self, sql):
        '''
        :param sql:"select * from information"
        :return:
        '''
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except:
            self.conn.rollback()


    def close(self):
        self.cursor.close()
        self.conn.close()


import hashlib
import datetime

class test:
    def __init__(self):
        self.hash = hashlib.md5()
        self.service =mysqlClient(conf ={'host': '101.132.113.50', 'port': 3306,'user': 'root','password': 'BlueSnail123!', 'db_name': 'spider_manage', 'table_name': 'webinfo'})

    def start(self,data):
        sql = 'insert into webinfo (id,url,add_time,agent,status,web_name,sort,info,checked) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # item = ('467f8ab6988134ffb76a24dbeeea0b98', 'https://finance.sina.com.cn/', '2019-04-17 14:23:04.906493', 0, 0, '新浪', 1, '')
        #
        # self.service.insert_data(sql, item)


        datas = []

        # data = [['人民网', 'http://finance.people.com.cn/'], ['中国日报', 'http://caijing.chinadaily.com.cn/'],
        #         ['CCTV', 'http://jingji.cctv.com/'], ['中华网', 'https://finance.china.com/'],
        #         ['中国人民广播电台', 'http://finance.cnr.cn/'], ['环球网', 'http://finance.huanqiu.com/'],
        #         ['光明网', 'http://economy.gmw.cn/'], ['参考消息', 'http://finance.cankaoxiaoxi.com/'],
        #         ['北方网', 'http://economy.enorth.com.cn/'], ['新浪', 'https://finance.sina.com.cn/'],
        #         ['中国经济网', 'http://www.ce.cn/'], ['凤凰网', 'http://finance.ifeng.com/'],
        #         ['西部网', 'http://finance.cnwest.com/'], ['网易新闻', 'http://money.163.com/'],
        #         ['中国新闻网', 'http://finance.chinanews.com/']]

        for item in data:
            cell = []
            self.hash.update(bytes(str(item[1]), encoding='utf-8'))
            cell.append(self.hash.hexdigest())
            cell.append(item[1])
            cell.append(str(datetime.datetime.now()))
            cell.append(0)
            cell.append(0)
            cell.append(item[0])
            cell.append(1)
            cell.append("")
            cell.append(0)

            print(tuple(cell))
            self.service.insert_data(sql, tuple(cell))



if __name__ =="__main__":
    # conf = {'host': '101.132.113.50', 'port': 3306, 'user': 'root', 'password': 'BlueSnail123!',
    #         'db_name': 'spider_manage', 'table_name': 'spider_task'}

    conf = {'host': '180.97.15.173', 'port': 3306, 'user': 'root', 'password': 'wzh234287',
            'db_name': 'crawler_task', 'table_name': 'weblinks'}
    service = mysqlClient(
        conf=conf)

    sql = "select webSite,requestUrl from weblinks "
    service.cursor.execute(sql)
    data = []
    for item in service.cursor.fetchall():
        data.append(list(item))
    t = test()
    t.start(data)
















