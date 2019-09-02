from celery import Celery

app = Celery('tasks', broker='redis://101.132.113.50:6379/8',backend='redis://101.132.113.50:6379/9')

@app.task
def add(x, y):
    return x + y