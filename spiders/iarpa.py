# -*- coding: utf-8 -*-

import requests
from lxml import etree
import time
from spiders.fanyi import translation

import pymysql
class DbToMysql(object):

    def __init__(self):
        self.con = pymysql.connect(
            host="180.97.15.173",
            user="wzh",
            password="wzh234287",
            db="bgnet",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        self.con.close()

    def save_one_data(self,datas):
        sql = "INSERT INTO `bgnet_intelligence` (person_id,collector_id,user_id,title,translat_title,hand_translat_title,type_way,type,translat_type,hand_translat_type,original_link,translat_original_link,hand_translat_original_link,web_site,translat_web_site,hand_translat_web_site,country,translat_country,hand_translat_country,content,translat_content,hand_translat_content,status,create_time,update_time,is_del,longitude,latitude,remark,mark) " \
              "VALUES ('0', NULL, NULL,'{0}' ,'{1}', NULL, 0, 0, NULL, NULL,'{2}', NULL, NULL, '{3}', NULL, NULL, '{4}', NULL, NULL, '{5}', '{6}', NULL, 0, '{7}', NULL, 0, '{8}', '{9}', NULL, NULL)".format(str(datas['title']),str(datas['translat_title']),datas['original_link'],datas['web_site'],datas['country'],str(datas['content']),str(datas['translat_content']),datas['create_time'],datas['longitude'],datas['latitude'])
        print(sql)
        try:
            with self.con.cursor() as cursor:
                print(cursor.execute(sql))
                self.con.commit()
        except Exception as e:
            return -1
        # finally:
        #     self.close()

dbsql = DbToMysql()


from dateutil.parser import parse as date_parser

'''
{   
    "title": "DoD Network Operations Face a Contested Environment", 
    "publish_time": "2019-05-03 00:00:00",
    "content": "", 
    "country": "\u7f8e\u56fd",
    "url": "https://fas.org/blogs/secrecy/2019/05/dod-network-ops/", 
    "source": "\u7f8e\u56fd\u79d1\u5b66\u5bb6\u8054\u76df"}



'''

# for i in range(10):
#     url = "https://www.dhs.gov/news-releases/press-releases?page={}".format(i)
#     html = requests.get(url).text
#     html_tree = etree.HTML(html)
#     herfs = html_tree.xpath("//span[@class= 'field-content']//a//@href")
#     news_herfs = ["https://www.dhs.gov"+item for item in herfs]
#     for sub_url in news_herfs:
#         data = {}
#         html = requests.get(sub_url).text
#         html_tree = etree.HTML(html)
#         data["title"] = str(html_tree.xpath("//h1//text()")[0]).replace("'","").replace("\"","")
#         data["translat_title"] = translation(data["title"])
#         timeArray = time.localtime(int(time.mktime(date_parser(html_tree.xpath("//meta[@property= 'article:published_time']//@content")[0]).timetuple())))
#         otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#         data["create_time"] = otherStyleTime
#         data["content"] = str(''.join(html_tree.xpath("//div[@class= 'field-items']//p//text()"))).replace("'","").replace("\"","")
#         try:
#             data["translat_content"] = translation(data["content"])
#         except:
#             data["translat_content"] = ""
#
#         data["country"] = "美国"
#         data["original_link"] = sub_url
#         data["longitude"] = 138.250000
#         data["web_site"] = "国土安全部"
#         data["latitude"] = 36.204824
#
#         dbsql.save_one_data(data)

