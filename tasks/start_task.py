from tasks.workers import app
from tasks import Crawleruning
from db.dao import SpiderTaskOper
spider_task = SpiderTaskOper()
@app.task(ignore_result=True)
def start_crawler(parameter):
    parameters = {}
    parameters["id"] = int(parameter)
    parameters = spider_task.start_task(parameters)

    crawler = Crawleruning()
    for item in parameters:
        crawler.set_parameter(item)
        crawler.start()


@app.task(ignore_result=True)
def excute_start_crawler(parameter):
    app.send_task('tasks.start_task.start_crawler', args=(parameter["id"],), queue='crawler_queue',
                          routing_key='for_crawler')