'''
https://www.gchq.gov.uk/
https://www.gchq.gov.uk/section/news/latestnews?q=&defaultTypes=news&sort=date%2Bdesc&start=0&rows=50
'''

import re
keywords = ["cyber", "securit", "Network", "leakag", "WikiLeak", "steal", "Confidential", "huawei", "secrecy", "hacker", "Espionag","Quantum","Intelligenc", "software", "gap", "cloud","antivirus","encryption","dns"]

import json

pattern = re.compile('|'.join(keywords), re.I)


from spiders import DbToMysql
import requests
from lxml import etree
import time
from dateutil.parser import parse as date_parser
from spiders.fanyi import translation

dbsql = DbToMysql()
for i in range(0,20):
    import requests

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.gchq.gov.uk/section/news/latestnews?q=&defaultTypes=news&sort=date%2Bdesc&start=0&rows=20',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Sec-Fetch-Mode': 'cors',
    }

    params = (
        ('q', ''),
        ('defaultTypes', 'news'),
        ('sort', 'date+desc'),
        ('start', '0'),
        ('rows', '{}'.format(i*10+10)),
    )

    html = requests.get('https://www.gchq.gov.uk/api/1/services/v1/search/query.json', headers=headers,
                            params=params).text

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://www.gchq.gov.uk/api/1/services/v1/search/query.json?q=&defaultTypes=news&sort=date%2Bdesc&start=0&rows=30', headers=headers)


    for item in json.loads(html).get("documents"):
    # print(titles)
    # print(times)
    # # for item in herfs:
    # #
    # #     print(etree.tostring(item))
    # # print(titles)
    # # print(times)
    #
    # for i in range(len(herfs)):
    #
        data = {}
        import requests

        headers = {
            'sec-fetch-mode': 'cors',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://www.gchq.gov.uk/news/location-of-new-gchq-site-in-manchester-revealed',
            'authority': 'www.gchq.gov.uk',
            'cookie': '_ga=GA1.3.2127389017.1571649330; _gid=GA1.3.1208874619.1571649330; _gat=1',
            'sec-fetch-site': 'same-origin',
        }

        params = (
            ('url', '{}'.format(item.get("pageUrl"))),
        )

        html = requests.get('https://www.gchq.gov.uk/api/1/services/v3/article-content.json', headers=headers,
                                params=params).text

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://www.gchq.gov.uk/api/1/services/v3/article-content.json?url=/news/location-of-new-gchq-site-in-manchester-revealed', headers=headers)

        # json.loads(html).get("content")
        content= json.loads(html).get("page").get("content").get("items")[0].get("description")

        data["title"] = str(item.get("title")).replace("'", "").replace("\"", "")
    #
    #
        data["content"] = str(content.replace("'","").replace("\"","").replace("<p>","\n").replace("</p>",""))
        try:
            # if len(pattern.findall( data["content"]+data["title"]))==0:
            #     continue
            data["translat_content"] = translation(data["content"])
        except:
            data["translat_content"] = ""
        timeArray = time.localtime(int(time.mktime(date_parser(item.get("date")).timetuple())))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data["create_time"] = otherStyleTime
        data["translat_title"] = translation(data["title"])
    #
        data["country"] = "美国"
        data["original_link"] ="https://www.gchq.gov.uk"+item.get("pageUrl")
        data["longitude"] = 138.250000
        data["web_site"] = "政府通讯总部"
        data["latitude"] = 36.204824
        print(data)
        dbsql.save_one_data(data)