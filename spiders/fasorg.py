import requests
from lxml import etree
import time,json
from spiders.fanyi import translation

# from dateutil.parser import parse as date_parser
# # for i in range(5,7):
# #     url = "https://fas.org/blogs/secrecy/page/{}/".format(i)
# #     html = requests.get(url).text
# #     html_tree = etree.HTML(html)
# #     herfs = html_tree.xpath("//article//header[@class= 'entry-header']//a[1]//@href")
# #     for sub_url in herfs:
# #         data = {}
# #         html = requests.get(sub_url).text
# #         html_tree = etree.HTML(html)
# #         data["title"] = html_tree.xpath("//h1[@class='entry-title']//text()")[0]
# #         timeArray = html_tree.xpath("//span[@class= 'date']//text()")[0]
# #         # timeArray = time.localtime(int(time.mktime(date_parser(timeArray).timetuple())))
# #
# #         # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# #         data["publish_time"] = timeArray
# #         data["content"] = ''.join(html_tree.xpath("//div[@class= 'entry-content']//p//text()"))
# #         data["country"] = "美国"
# #         data["url"] = sub_url
# #         data["source"] = "美国科学家联盟"
# #         import json
# #         print(json.dumps(data))

# for i in range(4,5):
#     url = "https://fas.org/blogs/security/page/{}/".format(i)
#     html = requests.get(url).text
#     html_tree = etree.HTML(html)
#     print(url)
#     herfs = html_tree.xpath("//article//header[@class= 'entry-header']//a[1]//@href")
#     for sub_url in herfs:
#         data = {}
#         html = requests.get(sub_url).text
#         html_tree = etree.HTML(html)
#         data["title"] = html_tree.xpath("//h1[@class='entry-title']//text()")[0]
#         timeArray = html_tree.xpath("//span[@class= 'date']//text()")[0]
#         # timeArray = time.localtime(int(time.mktime(date_parser(timeArray).timetuple())))
#
#         # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#         data["publish_time"] = timeArray
#         data["content"] = ''.join(html_tree.xpath("//div[@class= 'entry-content']//p//text()"))
#         data["country"] = "美国"
#         data["url"] = sub_url
#         data["source"] = "美国科学家联盟"
#         import json
#         print(json.dumps(data))
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
with open("data.json", "r+",encoding="utf-8") as fw:
    for item in fw.readlines():
        data = {}
        item = json.loads(item)
        url = item["url"]
        source = item["source"]
        article_title = item["title"]

        article_text = item["content"]
        data["title"] = str(article_title).replace("'", "").replace("\"", "")
        try:

            data["translat_title"] = translation(data["title"])
        except:
            data["translat_title"] = ""
        data["create_time"] = item["publish_time"]
        data["content"] = str(article_text).replace("'", "").replace(
            "\"", "")
        try:
            data["translat_content"] = translation(data["content"])
        except:
            data["translat_content"] = ""

        data["country"] = "美国"
        data["original_link"] = url
        data["longitude"] = 138.250000
        data["web_site"] = source
        data["latitude"] = 36.204824
        print(data)
        dbsql.save_one_data(data)