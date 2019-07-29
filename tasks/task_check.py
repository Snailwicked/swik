# coding:utf-8
import time

from tasks.workers import app
from utils.spiderutils.parse import Parse
@app.task(ignore_result=True)
def check_task(urls):
    parse = Parse()
    result = parse.get_data(urls)


@app.task(ignore_result=True)
def excute_check_task(urls):
        app.send_task('tasks.task_check.check_task', args=(urls), queue='check_queue',
                      routing_key='for_check')
