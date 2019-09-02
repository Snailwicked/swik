from config import *
from tasks.workers import app
from tasks import Crawleruning
from db.dao import SpiderTaskOper
spider_task = SpiderTaskOper()
@app.task(ignore_result=True)
def start_crawler(parameter):
    parameters = {}
    parameters["id"] = parameter
    params = spider_task.start_task(parameters)
    for item in params:
        crawler = Crawleruning()
        crawler.set_parameter(item)
        crawler.start()
    crawler_info.info("已经更改爬虫状态")
    parameters["status"] = 0
    spider_task.update_status(parameters)

@app.task(ignore_result=True)
def excute_start_crawler(parameter):
    crawler_info.info("Task started!")
    result = app.send_task('tasks.start_task.start_crawler', args=(parameter["id"],), queue='crawler_queue',
                          routing_key='for_crawler')
    crawler_info.info(result.task_id)
    return result.task_id


