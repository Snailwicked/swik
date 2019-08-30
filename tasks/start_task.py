from config import *
from tasks.workers import app
from tasks import Crawleruning
from db.dao import SpiderTaskOper
spider_task = SpiderTaskOper()
@app.task(ignore_result=True)
def start_crawler(parameter):
    crawler_info.info(parameter)
    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()


@app.task(ignore_result=True)
def excute_start_crawler(parameter):
    crawler_info.info("Task started!")
    parameters = spider_task.start_task(parameter)
    for item in parameters:
        app.send_task('tasks.start_task.start_crawler', args=(item,), queue='crawler_queue',
                          routing_key='for_crawler')

