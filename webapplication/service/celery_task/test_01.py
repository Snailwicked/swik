from celery import Celery

celery = Celery('myapp', broker='redis://guest@localhost//')

@celery.task
def add(x, y):
    return x + y