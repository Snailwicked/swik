# coding:utf-8

from tasks.workers import app
from utils.base_utils.down import Crawling
@app.task(ignore_result=True)
def check_crawler(parameters):
    crawler = Crawling()
    crawler.set_parameters(parameters)
    crawler.run()


@app.task(ignore_result=True)
def excute_check_crawler(parameters):
        app.send_task('tasks.crawler_check.check_crawler', args=(parameters), queue='crawler_queue',
                      routing_key='for_crawler')
