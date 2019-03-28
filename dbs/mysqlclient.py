# -*- coding: utf-8 -*-
import pymysql

'''mysql 客户端封装接口'''
class mysqlClient():
    def __init__(self):
        self.mysql_conf = {'host': '182.254.198.218', 'port': 3306, 'user': 'root', 'password': 'vrv123123',
                           'db_name': 'crawler',
                           'db_table': 'information'}

        self.conn = pymysql.connect(host=self.mysql_conf['host'], port=self.mysql_conf['port'],
                                    user=self.mysql_conf['user'], passwd=self.mysql_conf['password'],
                                    db=self.mysql_conf['db_name'], charset="utf8")
        self.cursor = self.conn.cursor()

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


    def close_all(self):
         try:
             if self.cursor is not None:
                 self.cursor.close()
                 self.conn.close()
         finally:
             if self.cursor is not None:
                 self.cursor.close()
                 self.conn.close()
