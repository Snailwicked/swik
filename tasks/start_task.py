from tasks.workers import app
from tasks import Crawleruning
@app.task(ignore_result=True)
def start_crawler(parameters):
    crawler = Crawleruning()
    crawler.set_parameter(parameters)
    crawler.start()


@app.task(ignore_result=True)
def excute_start_crawler(parameters):
        app.send_task('tasks.start_task.start_crawler', args=(parameters), queue='crawler_queue',
                      routing_key='for_crawler')