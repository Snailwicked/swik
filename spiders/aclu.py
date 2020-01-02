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
https://www.aclu.org/blog-feed/people-power?page=0     人民力量
https://www.aclu.org/blog-feed/breaking-news?page=0    爆炸新闻
https://www.aclu.org/blog-feed/editors-picks?page=0    编辑精选
https://www.aclu.org/blog/speak-freely?page=0          自由发言
https://www.aclu.org/blog/free-future
https://www.aclu.org/blog/the-campaign
https://www.aclu.org/blog-feed/gamut
https://www.aclu.org/press-releases
'''


for i in range(20):

    url = "https://www.aclu.org/press-releases?page={}".format(i)
    print(url)
    html = requests.get(url).text
    html_tree = etree.HTML(html)
    herfs = html_tree.xpath("//div[@id= 'main']//div[contains(@class,'views-row views')]//h3//a//@href")
    titles = html_tree.xpath("//div[@id= 'main']//div[contains(@class,'views-row views')]//h3//a//text()")
    times = html_tree.xpath("//div[@id= 'main']//div[contains(@class,'views-row views')]//span[@class='date']//text()")
    print(herfs)
    print(titles)
    print(times)

    for i in range(len(herfs)):
        data = {}
        html = requests.get("https://www.aclu.org"+herfs[i]).text
        html_tree = etree.HTML(html)
        data["title"] = str(titles[i]).replace("'","").replace("\"","")
        data["translat_title"] = translation(data["title"])
        timeArray = time.localtime(int(time.mktime(date_parser(times[i]).timetuple())))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data["create_time"] = otherStyleTime
    #
    #

        data["content"] = str(''.join([item + "\n" for item in html_tree.xpath("//div[@class= 'inner']//p//text()")]).replace("'","").replace("\"",""))
        try:
            data["translat_content"] = translation(data["content"])
        except:
            data["translat_content"] = ""

        data["country"] = "美国"
        data["original_link"] = "https://www.aclu.org"+herfs[i]
        data["longitude"] = 138.250000
        data["web_site"] = "美国公民自由联盟"
        data["latitude"] = 36.204824
        print(data)
        dbsql.save_one_data(data)

