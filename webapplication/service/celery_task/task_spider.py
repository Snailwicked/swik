from celery import Celery
import time

app = Celery('tasks', broker='redis://101.132.113.50:6379/0',backend ='redis://101.132.113.50:6379/0' )
@app.task(name="tasks.adds")
def add(x, y):
    time.sleep(3) # 模拟耗时操作
    s = x + y
    return s

