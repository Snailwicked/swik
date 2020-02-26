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
                if fields.get("publishTime"):
                    try:
                        from dateutil.parser import parse as date_parser
                        import time
                        date_str = xpath.get_contents(fields.get("publishTime").replace("+", "@"))
                        item["publish_time"] = int(time.mktime(date_parser(date_str[0]).timetuple()) * 1000)
                    except:
                        item["publish_time"] = int(content_extractor.get_publishing_date())
                else:
                    item["publish_time"] = int(content_extractor.get_publishing_date())
                if fields.get("title"):
                    item["title"] = xpath.get_contents(fields.get("title"))
                else:
                    item["title"] = content_extractor.get_title()

                if fields.get("author"):
                    try:
                        item["author"] = "".join(xpath.get_contents(fields.get("author"))).replace("\r","").replace("\n","")
                    except:
                        item["authors"] = content_extractor.get_authors()
                else:
                    item["authors"] = content_extractor.get_authors()

                # if item["authors"]=="":
                #     item["authors"] = content_extractor.get_authors()

                if fields.get("content"):
                    try:
                        result = xpath.get_contents(fields.get("content"))
                        results = "".join(
                            list(map(lambda string: (string + "<br /><br />") if len(string) > 10 else (string), result)))

                        item["content"] = results
                    except:
                        item["content"] = content_extractor.get_content()
                else:
                    item["content"] = content_extractor.get_content()
                # if item["content"] == "":
                #     item["content"] = content_extractor.get_content()


                item["collection_time"] = int(content_extractor.get_thirteenTime())
                item["summary"] = ""
                item["source"] = parameter["webSite"]
            except Exception as e:
                crawler_info.info("parseing of Failed {} {}".format(parameter["url"],e))
                continue
            print(item)
            new_data.insert(item)



if __name__ == "__main__":
    import time
    # start_time = time.time()
    # urls = [{'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                  'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #         'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}, {
    #            'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
    #                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957,
    #            'webSite': '扬州网', 'url': 'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm'}]
    #
    # parse = Parse()
    # parse.get_data(urls)
    # end_time = time.time()
    # print(end_time-start_time)
    from dateutil.parser import parse as date_parser

    print(int(time.mktime(date_parser("2019年11月15日 14:51:34").timetuple()) * 1000))
    # urls = []
    # str_url = "http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm"
    #
    # for i in range(10):
    #     urls.append(str_url)
    # print("urls = ",urls)