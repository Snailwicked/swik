from utils.slave import ContentExtractor
from utils.spider_utils.xpathtexts import xPathTexts
from utils.exception_utils import parse_text
from db import News_data
from config import *
xpath = xPathTexts()
new_data =News_data()
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
                fields = parameter.get("rule").get("fields")

                item["url"] = parameter["url"]

                if fields.get("title"):
                    item["title"] = xpath.get_contents(fields.get("title"))
                else:
                    item["title"] = content_extractor.get_title()

                if fields.get("author"):
                    item["author"] = xpath.get_contents(fields.get("author"))
                else:
                    item["authors"] = content_extractor.get_authors()

                if fields.get("content"):
                    item["content"] = xpath.get_contents(fields.get("content"))
                else:
                    item["content"] = content_extractor.get_content()

                if fields.get("publish_time"):
                    item["publish_time"] = xpath.get_contents(fields.get("publish_time"))
                else:
                    item["publish_time"] = int(content_extractor.get_publishing_date())

                item["collection_time"] = int(content_extractor.get_thirteenTime())
                item["summary"] = content_extractor.get_summary()
                item["source"] = parameter["webSite"]
            except Exception as e:
                crawler_info.info("parseing of Failed {}".format(parameter["url"]))
                continue
            # crawler_info.info(item)
            print(item)
            # new_data.insert(item)



if __name__ == "__main__":
    import time
    start_time = time.time()
    urls = [{'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
               'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                        'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
               'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}]

    parse = Parse()
    parse.get_data(urls)
    end_time = time.time()
    print(end_time-start_time)

    # urls = []
    # str_url = "http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm"
    #
    # for i in range(10):
    #     urls.append(str_url)
    # print("urls = ",urls)
