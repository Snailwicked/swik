from core import AttrField, Item, Request, Spider
from utils.slave import ContentExtractor
from utils.spider_utils.xpathtexts import xPathTexts
xpath = xPathTexts()

class NewsSpider(Spider):
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10
    async def parse(self, res):
        print(res.html)





if __name__ == '__main__':
    import time
    start_time = time.time()
    parameter = {'rule': {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
              'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}, 'pid': 5957, 'webSite': '扬州网',
     'url': 'http://www.yznews.com.cn/'}
    urls = ['http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm',
            'http://meishi.yznews.com.cn/2019-09/09/content_7066513.htm']
    NewsSpider.start_urls = urls
    NewsSpider.start()
    end_time = time.time()
    print(end_time-start_time)