# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from spider.items import SpiderItem
# from spider.utils.parse_content import ParseContent
# from spider.utils.parse_other import ParseOther
import json
class StaticNewsSpider(CrawlSpider):
    name = 'static_html'
    def __init__(self, rule):
        self.rule = rule
        self.main_url = rule.get("main_url")
        self.start_urls = []
        self.start_urls.append(self.main_url)
        print()
        rule_list = []
        rule_list.append(Rule(LinkExtractor(
            allow=[str(rule.get("re_url").get('re0'))]),
            callback='parse_item'))
        self.rules = tuple(rule_list)
        super(StaticNewsSpider, self).__init__()



    def parse_item(self, response):
        newsurl = response.url
        print(newsurl)
        # parsecontent = ParseContent(url=newsurl)
        # parseother = ParseOther(url=newsurl)
        # try:
        #     content = parsecontent.getContext()
        # except Exception as e:
        #     content = ''
        #     print('解析文章内容出错:{}, 页面URL{}'.format(e, newsurl))
        #
        # try:
        #     author = parseother.get_author()
        # except Exception as e:
        #     author = ''
        #     print('解析文章作者出错:{}, 页面URL{}'.format(e, newsurl))
        #
        # try:
        #     publishTime = parseother.get_publishTime()
        # except Exception as e:
        #     publishTime = ""
        #     print('解析文章发布时间出错:{}, 页面URL{}'.format(e, newsurl))
        #
        # try:
        #     title = parseother.get_title()
        # except Exception as e:
        #     title = ""
        #     print('解析文章标题出错:{}, 页面URL{}'.format(e, newsurl))
        #
        # try:
        #     collectTime = parseother.get_collectTime()
        # except Exception as e:
        #     collectTime = ""
        #     print('获取文章采集时间出错:{}, 页面URL{}'.format(e, newsurl))
        # print(newsurl)
        # item = SpiderItem(author=author, publishTime=publishTime, title=title, collectTime=collectTime,
        #                   newsurl=newsurl, content=content)
        # yield item
