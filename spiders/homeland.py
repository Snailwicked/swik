import requests
from lxml import etree
import time

from dateutil.parser import parse as date_parser
monitor_words =  ["cyber","cybersecurity","network security","information security","Cyberspace policy","Network vulnerability","Cyber warfare","Network attacks","cyber attack","Data leakage","Network  security standard","guideline","Cyber security publication","WikiLeaks","steal secret","Stealing technology","disclose a secret","Confidential"]
for i in range(10):
    url = "https://www.dhs.gov/news-releases/press-releases?page={}".format(i)
    html = requests.get(url).text
    html_tree = etree.HTML(html)
    herfs = html_tree.xpath("//span[@class= 'field-content']//a//@href")
    news_herfs = ["https://www.dhs.gov"+item for item in herfs]
    for sub_url in news_herfs:
        data = {}
        html = requests.get(sub_url).text
        html_tree = etree.HTML(html)
        data["title"] = html_tree.xpath("//h1//text()")[0]
        timeArray = time.localtime(int(time.mktime(date_parser(html_tree.xpath("//meta[@property= 'article:published_time']//@content")[0]).timetuple())))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data["publish_time"] = otherStyleTime
        data["content"] = ''.join(html_tree.xpath("//div[@class= 'field-items']//p//text()"))
        for item in monitor_words:
            if item in data["content"]:
                data["country"] = "美国"
                data["url"] = sub_url
                data["source"] = "国土安全部"
                print(data)
            continue
