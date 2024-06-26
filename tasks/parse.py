# -*- coding: utf-8 -*-
from utils.slave import ContentExtractor
from utils.spider_utils.xpathtexts import xPathTexts
from utils.exception_utils import parse_text
from db import News_data
from config import *
xpath = xPathTexts()
new_data =News_data()
import hashlib
hash = hashlib.md5()
from urllib.parse import urlparse
import time

class Parse:
    def __int__(self):
        self.parameters = None
    @parse_text
    def get_data(self, parameters):
        if not isinstance(parameters, list):
            temp = []
            temp.append(parameters)
            self.parameters = temp
        else:
            self.parameters =  parameters

        for parameter in self.parameters:
            item= {}
            try:
                xpath.set_parameter(url=parameter["url"])
                if xpath.html == None:
                    continue
                content_extractor = ContentExtractor(html=xpath.html, url=parameter["url"])
                import json
                fields = parameter.get("rule").get("fields")
                item["url"] = parameter["url"]
                url_netloc = urlparse(item["url"])
                item["domain"] = url_netloc.netloc

                hash.update(bytes(parameter["url"], encoding='utf-8'))
                item["id"] = hash.hexdigest()

                if fields.get("title"):
                    item["title"] = xpath.get_contents(fields.get("title").replace("+","@"))
                else:
                    item["title"] = content_extractor.get_title()

                if fields.get("author"):
                    item["author"] = xpath.get_contents(fields.get("author").replace("+","@"))
                else:
                    item["authors"] = content_extractor.get_authors()

                if fields.get("content"):
                    result = xpath.get_contents(fields.get("content").replace("+","@"))
                    results = "".join(
                        list(map(lambda string: (string + "<br /><br />") if len(string) > 10 else (string), result)))

                    item["content"] = results
                else:
                    item["content"] = content_extractor.get_content()

                if item["content"] =="":
                    item["content"] = content_extractor.get_content()

                if fields.get("publish_time"):
                    from dateutil.parser import parse as date_parser
                    date_str = xpath.get_contents(fields.get("publish_time").replace("+","@"))
                    item["poTime"] = int(time.mktime(date_parser(date_str).timetuple()) * 1000)

                else:
                    item["poTime"] = int(content_extractor.get_publishing_date())
                millis = int(item["poTime"]/1000)
                datetime_str = time.strftime('%Y%m%d%H', time.localtime(millis))
                item["poMonth"] = int(datetime_str[0:6])
                item["poDay"] = int(datetime_str[0:8])
                item["poHour"] = int(datetime_str)
                item["addTime"] = int(content_extractor.get_thirteenTime())
                item["source"] = parameter["webSite"]
                item["pr"] = 0
                item["webSiteType"] = 1
                item["webSite"] = parameter["webSite"]
                item["positiveOrNegative"] =0
                item["abroad"] = 0
                item["spreadValue"] = 0
                item["replay"] = 0
                item["view"] = 0
                item["importanceDegree"] = 0
                item["opinionValue"] = 0
                item["sensitiveValue"] = 0
                item["snapshotAddress"] = ""
                item["administrativeId"] = "000000"
                item["titlePrint"] = ""
                item["titleContentPrint"] = ""
                item["img"] = ""
                item["moodValue"] = 0
                item["uuid"] = content_extractor.get_uuid()
                item["updateFrequency"] = 0
                item["suggest"] = ""
                item["rubbish"] = 0
                item["importantValue"] = 0
                item["provinceCode"] = 0
            except Exception as e:
                crawler_info.info("parseing of Failed {},{}".format(parameter["url"],e))
                continue
            # crawler_info.info(item)
            print(item)

            return item
            # new_data.insert(item)



if __name__ == "__main__":
    parse = Parse()
    url = {'url': 'http://www.qstheory.cn/wp/2020-01/14/c_1125460341.htm','rule': {'filter_rule': '/\\\\d{4}-\\\\d{2}/\\\\d{2}/c_\\\\d{10}.htm', 'selector': 'xpath选择器', 'deep_limit': '1',
              'fields': {'title': '', 'author': '', 'publishTime': '',
                         'content': '//div[@class="highlight"]//p//text()'}}, 'webSite': '测试'}

    parse.get_data(url)
    #   ParseRparseesult(scheme='http', netloc='www.chenxm.cc', path='/post/719.html', params='', query='', fragment='')


    # import time
    # start_time = time.time()
    # urls = [{'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                  'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #         'webSite': '扬州网', 'url': 'https://www.jinse.com/blockchain/564581.html'},]
    # # {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    # #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    # #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    # #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}]
    # #
    # parse = Parse()
    # parse.get_data(urls)
    # end_time = time.time()
    # print(end_time-start_time)

    # urls = []
    # str_url = "http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm"
    #
    # for i in range(10):
    #     urls.append(str_url)
    # print("urls = ",urls)
