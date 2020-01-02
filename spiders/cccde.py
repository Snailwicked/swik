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
https://www.ccc.de/de/?page=2
'''

for i in range(1,2):

    url = "https://www.ccc.de/de/?page={}".format(i)
    print(url)
    html = requests.get(url).text
    html_tree = etree.HTML(html)
    herfs = html_tree.xpath("//div[@class = 'article_partial']//h2//a//@href")
    # herfs = [item.xpath("a//@href")[0] for item in herfs]
    titles =  html_tree.xpath("//div[@class = 'article_partial']//h2//a//text()")
    times =  html_tree.xpath("//div[@class = 'article_partial']//div[@class= 'author_and_date']//text()")

    print(herfs)
    print(titles)
    # times = html_tree.xpath("//span[@class= 'pub-date']//text()")
    new_times= []
    for item in times:
        itemarry = str(item).replace("\\n",'').strip().split(",")
        if itemarry:
            new_times.append(itemarry[0])
    print(new_times)

    for i in range(len(herfs)):
        data = {}
        html = requests.get("https://www.ccc.de"+herfs[i]).text
        html_tree = etree.HTML(html)
        data["title"] = str(str(titles[i]).strip()).replace("'","").replace("\"","")
        data["translat_title"] = translation(data["title"])
        try:
            timeArray = time.localtime(int(time.mktime(date_parser(str(new_times[i]).replace("\\n","").replace("\\t","")).timetuple())))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        except:
            print("出现异常")
            continue
        data["create_time"] = otherStyleTime
    # # # #
    # # # # #
    # # # #
        data["content"] = str(''.join([item + "\n" for item in html_tree.xpath("//div[@class= 'article']//p//text()")]).replace("'","").replace("\"",""))
        try:
            data["translat_content"] = translation(data["content"])
        except:
            data["translat_content"] = ""
    #
        data["country"] = "美国"
        data["original_link"] = "https://www.ccc.de"+herfs[i]
        data["longitude"] = 138.250000
        data["web_site"] = "Chaos-computer-club"
        data["latitude"] = 36.204824
        print(data)
        dbsql.save_one_data(data)

