import requests
from spiders.fanyi import translation
import time
from dateutil.parser import parse as date_parser
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
headers = {
    'sec-fetch-mode': 'cors',
    'cookie': 'fastlyCountryCode=CN; _sp_enable_dfp_personalized_ads=true; consentUUID=bf5e640e-d2a7-4122-9929-0595cc12d12f; firstSessionDate=Sun, 29 Sep 2019 02:35:52 GMT; BCSessionID=9dc286f7-037c-4e68-ab4d-2cf1f696e14d; _ntv_uid=17cd5e0a-e406-485c-9bc8-e732320a41fa; __gads=ID=c6f55f2110c3f592:T=1569724553:S=ALNI_MYVExH1Ga2rch-MYTzeckehBrmS_w; permutive-id=12f5b7a4-7adf-40f9-b954-2e7d9f4d5463; _ga=GA1.2.344427816.1569724552; sessionNumber=2; selectedLocale=0; aiia=true; currentSessionDate=Tue, 15 Oct 2019 07:17:39 GMT; lastSessionDate=Mon, 14 Oct 2019 05:52:11 GMT; inSession=true; _gid=GA1.2.794291988.1571123891; last_visit_bc=1571124262355; permutive-session=%7B%22session_id%22%3A%2213d5fde9-2c6b-4288-b54f-57276c12b1a8%22%2C%22last_updated%22%3A%222019-10-15T07%3A24%3A23.095Z%22%7D; AMP_TOKEN=%24ERROR; _gat_UA-300704-1=1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'accept': 'text/html, */*; q=0.01',
    'referer': 'https://www.computerworld.com/category/security/',
    'authority': 'www.computerworld.com',
    'x-requested-with': 'XMLHttpRequest',
    'sec-fetch-site': 'same-origin',
}
from lxml import etree

for i in range(1):
    params = (
        ('def', 'loadMoreList'),
        ('pageType', 'index'),
        ('catId', '2206'),
        ('category', '2206'),
        ('days', '-730'),
        ('pageSize', '10'),
        ('offset', '0'),
        ('ignoreExcludedIds', 'true'),
        ('brandContentOnly', 'false'),
        ('includeBlogTypeIds', '1,3'),
        ('includeVideo', 'true'),
        ('liveOnly', 'true'),
        ('includeMediaResource', 'true'),
        ('isInsiderIndex', 'true'),
        ('sortOrder', 'date'),
        ('locale_id', '0'),
        ('startIndex', '{}'.format(i*20+10)),
    )



    response = requests.get('https://www.computerworld.com/napi/tile', headers=headers, params=params)
    print(response.url)
    html = response.text
    html_tree = etree.HTML(html)
    herfs = html_tree.xpath("//div[@class= 'river-well article']//div[@class='post-cont']//h3//a//@href")
    titles = html_tree.xpath("//div[@class= 'river-well article']//div[@class='post-cont']//h3//a//text()")

    for i in range(len(herfs)):
        data = {}
        html = requests.get("https://www.computerworld.com"+herfs[i]).text
        html_tree = etree.HTML(html)
        data["title"] = str(titles[i]).replace("'","").replace("\"","")
        data["translat_title"] = translation(data["title"])
        timeArray = time.localtime(int(time.mktime(date_parser(html_tree.xpath("//span[@class= 'pub-date']//@content")[0]).timetuple())))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data["create_time"] = otherStyleTime
    #
    #

        data["content"] = str(''.join([item + "\n" for item in html_tree.xpath("//div[@id= 'drr-container']//p//text()")]).replace("'","").replace("\"",""))
        try:
            data["translat_content"] = translation(data["content"])
        except:
            data["translat_content"] = ""

        data["country"] = "美国"
        data["original_link"] = "https://www.computerworld.com" + herfs[i]
        data["longitude"] = 138.250000
        data["web_site"] = "Security-Topic-Center–Computerworld"
        data["latitude"] = 36.204824
        print(data)
        dbsql.save_one_data(data)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.computerworld.com/napi/tile?def=loadMoreList&pageType=index&catId=2206&category=2206&days=-730&pageSize=20&offset=0&ignoreExcludedIds=true&brandContentOnly=false&includeBlogTypeIds=1%2C3&includeVideo=true&liveOnly=true&includeMediaResource=true&isInsiderIndex=true&sortOrder=date&locale_id=0&startIndex=44', headers=headers)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.computerworld.com/napi/tile?def=loadMoreList&pageType=index&catId=2206&category=2206&days=-730&pageSize=20&offset=0&ignoreExcludedIds=true&brandContentOnly=false&includeBlogTypeIds=1%2C3&includeVideo=true&liveOnly=true&includeMediaResource=true&isInsiderIndex=true&sortOrder=date&locale_id=0&startIndex=22', headers=headers)
