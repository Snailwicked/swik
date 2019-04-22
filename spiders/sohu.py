 # -*- coding: utf-8 -*-
import time,hashlib
import requests,re
from lxml import etree
import pymysql
import datetime

headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',}


class mysqlClient():
    def __init__(self):
        self.mysql_conf = {'host': '182.254.198.218', 'port': 3306, 'user': 'root', 'password': 'vrv123123',
                           'db_name': 'crawler',
                           'db_type': 'information'}

        self.conn = pymysql.connect(host=self.mysql_conf['host'], port=self.mysql_conf['port'],
                                    user=self.mysql_conf['user'], passwd=self.mysql_conf['password'],
                                    db=self.mysql_conf['db_name'], charset="utf8")
        self.cursor = self.conn.cursor()

    def insert_data(self, sql,data):
        try:
            self.cursor.execute(sql,data)
            print("插入成功")

            self.conn.commit()
        except:
            print("该数据已存在数据库中")
            self.conn.rollback()


class crawler(object):
    '''通用定向爬虫'''
    def __init__(self, url = None,X_path=None ,header = None):
        self.url = url
        self.X_path = X_path
        self.contents = []
        self.headers = header

    def getHtml(self):
        print(self.url)
        resp = requests.get(self.url,headers= self.headers)
        charset = None
        try:
            reg = '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?'
            bianma = re.findall(reg, resp.text)[0][1]
        except:
            bianma = ""
        if bianma!="":
            charset = bianma.lower()
        resp.encoding = charset
        return resp.text

    def get_contents(self,url,X_path,header):
        self.url = url
        self.X_path = X_path
        self.contents = []
        self.headers = header
        self.html = self.getHtml()
        contens = []
        for item in etree.HTML(str(self.html)).xpath(self.X_path):
            contens.append(str(item).strip())
        return contens


class souhuNews(crawler):
    def __init__(self,url):
        super(souhuNews, self).__init__()
        self.starturl = url
        self.headers = headers
        self.session = requests.session()
        self.session.headers = headers
        self.hash = hashlib.md5()
        self.service = mysqlClient()

        # self.rediscon = RedisClient()

    def start_spider(self):
        try:
            json_all_str = self.session.get(url=self.starturl).text
        except:
            print("搜狐网站停止提供数据")
        self.__handle_data(json_all_str)


    def timestamp_to_date(self,time_stamp):
        import math
        time_array = time.localtime(math.floor(time_stamp/1000)+time_stamp%1000/1000)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return otherStyleTime

    def __handle_data(self,json_all_str):
        json_all_str = re.sub('null|false|true', 'None', json_all_str)
        data_all_list = eval(json_all_str)
        for item in data_all_list:
            data = []
            id = item['id']
            author_id = item['authorId']
            author = item['authorName']
            title = item['title']
            publicTime = item['publicTime']
            url = 'http://www.sohu.com/a/{0}_{1}'.format(id, author_id)
            X_path = "//article[@class = 'article']//p//text()"
            content = "".join(self.get_contents(url, X_path, headers))
            self.hash.update(bytes(url, encoding='utf-8'))
            data.append(2)
            data.append(url)
            data.append(author)
            data.append(title)
            data.append(content)
            data.append(self.timestamp_to_date(publicTime))
            data.append(str(datetime.datetime.now()))
            print(self.timestamp_to_date(time.time()))
            data.append(self.hash.hexdigest())
            sql_insert = 'insert into information (`type`, url,author,title,content,postTime,addtime,`unique`) values (%s,%s,%s,%s,%s,%s,%s,%s)'
            print(tuple(data))
            self.service.insert_data(sql_insert, tuple(data))


if __name__ == "__main__":
    url = 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=10&page=1&size=1000'
    souhu = souhuNews(url=url)
    souhu.start_spider()


