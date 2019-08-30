# # coding:utf-8
import os
#
from celery import Celery, platforms
from config.conf import get_broker_and_backend
platforms.C_FORCE_ROOT = True
broker, backend = get_broker_and_backend()
#
tasks = ['tasks.start_task']

app = Celery('spider_task', include=tasks, broker=broker, backend=backend)
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES={
        'tasks.start_task.excute_start_crawler':
            {
                'queue': 'crawler_queue',
                'routing_key': 'crawler_queue'
            },

        'tasks.start_task.excute_parse_url':
            {
                'queue': 'parse_queue',
                'routing_key': 'parse_queue'
            },

    },

    CELERY_QUEUES={
        "crawler_queue": {
            "exchange": "crawler_queue",
            "exchange_type": "direct",
            "routing_key": "crawler_queue"
        },
        "parse_queue": {
            "exchange": "parse_queue",
            "exchange_type": "direct",
            "routing_key": "parse_queue"
        },

    }

)






