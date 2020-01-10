from config import *
from tasks.workers import app
from tasks.accurate_crawler  import Crawleruning
from db.dao import SpiderTaskOper
spider_task = SpiderTaskOper()
from tasks.parse import Parse
parse = Parse()
from db.redis_db import Url_Parameter
url_parameter = Url_Parameter
@app.task(ignore_result=True)
def start_crawler(parameter):
    parameters = {}
    parameters["id"] = parameter
    key = 1
    while key:
        urls = url_parameter.fetch_parameters("parameter")

        if len(urls)!=0:
            for item in urls:
                '''
                 item = {'rule': {
                             'filter_rule': '',
                             'selector': 'xpath',
                             'deep_limit': '1',
                             'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}
                         },
                 'pid': 6041,
                 'webSite': '新华网舆情',
                 'url': 'http://www.news.cn/yuqing/index.htm'
                 }
        
                '''
                import json
                item = json.loads(item)
                crawler = Crawleruning()
                crawler.set_parameter(item)
                crawler.start()
                target_url = crawler.process()
                for sub_url in target_url:
                    item["url"] = sub_url
                    app.send_task('tasks.start_task.parse_url',
                                  args=(item,),
                                  queue='crawler_queue',
                                  routing_key='for_crawler')
        else:
            params = spider_task.start_task(parameters)
            for param in params:
                url_parameter.store_parameter("parameter",param)
    # parameters["status"] = 0
    # spider_task.update_status(parameters)


@app.task(ignore_result=True)
def parse_url(parameter):
    import time
    time.sleep(1)
    item = parse.get_data(parameter)
    # with topic.get_producer() as producer:
    #     string = bytes(str(json.dumps(item)), encoding='utf-8')
    #     producer.produce(string)

@app.task(ignore_result=True)
def excute_start_crawler(parameter):
    crawler_info.info("Task started!")
    result = app.send_task('tasks.start_task.start_crawler', args=(parameter["id"],), queue='crawler_queue',
                          routing_key='for_crawler')
    crawler_info.info(result.task_id)
    return result.task_id


