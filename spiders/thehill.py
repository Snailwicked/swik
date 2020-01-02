'''
https://thehill.com/homenews/senate?page=0
https://thehill.com/homenews/house?page=1
https://thehill.com/homenews/administration?page=1
https://thehill.com/homenews/campaign?page=1
https://thehill.com/business-a-lobbying?page=1
'''
import re
keywords = ["cyber", "securit", "Network", "leakag", "WikiLeak", "steal", "Confidential", "huawei", "secrecy", "hacker", "Espionag","Quantum","Intelligenc", "software", "gap", "cloud","antivirus","encryption","dns"]



pattern = re.compile('|'.join(keywords), re.I)


from spiders import DbToMysql
import requests
from lxml import etree
import time
from dateutil.parser import parse as date_parser
from spiders.fanyi import translation

dbsql = DbToMysql()
for i in range(40,60):
    url = "https://thehill.com/homenews/campaign?page={}".format(i)
    print(url)
    html = requests.get(url).text
    html_tree = etree.HTML(html)
    herfs = html_tree.xpath("//div[@class= 'view-content']//div//article//header//h2//a//@href")

    titles = html_tree.xpath("//div[@class= 'view-content']//div//article//header//h2//a//text()")
    times = html_tree.xpath("//div[@class= 'view-content']//div//article//header//p//span[@class = 'date']//text()")
    print(herfs)
    # print(titles)
    # print(times)
    # # for item in herfs:
    # #
    # #     print(etree.tostring(item))
    # # print(titles)
    # # print(times)
    #
    for i in range(len(herfs)):

        data = {}
        html = requests.get("https://thehill.com"+herfs[i]).text
        html_tree = etree.HTML(html)
        data["title"] = str(titles[i]).replace("'", "").replace("\"", "")


        data["content"] = str(''.join([item + "\n" for item in html_tree.xpath("//div[@class= 'field-items']//p//text()")]).replace("'","").replace("\"",""))
        try:
            if len(pattern.findall( data["content"]+data["title"]))==0:
                continue
            data["translat_content"] = translation(data["content"])
        except:
            data["translat_content"] = ""
        timeArray = time.localtime(int(time.mktime(date_parser(times[i]).timetuple())))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data["create_time"] = otherStyleTime
        data["translat_title"] = translation(data["title"])

        data["country"] = "美国"
        data["original_link"] = "https://thehill.com"+herfs[i]
        data["longitude"] = 138.250000
        data["web_site"] = "TheHill"
        data["latitude"] = 36.204824
        print(data)
        dbsql.save_one_data(data)