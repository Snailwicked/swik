# # coding:utf-8
import os
#
from celery import Celery, platforms
from config.conf import get_broker_and_backend
platforms.C_FORCE_ROOT = True
broker, backend = get_broker_and_backend()
#
tasks = ['tasks.task_check',"tasks.crawler_check"]

app = Celery('spider_task', include=tasks, broker=broker, backend=backend)

app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES={
        'tasks.task_check.excute_check_task':
            {
                'queue': 'check_queue',
                'routing_key': 'check_queue'
            },

        'tasks.crawler_check.excute_check_crawler':
            {
                'queue': 'crawler_queue',
                'routing_key': 'crawler_queue'
            },

    },

    CELERY_QUEUES={
        "check_queue": {
            "exchange": "check_queue",
            "exchange_type": "direct",
            "routing_key": "check_queue"
        },
        "crawler_queue": {
            "exchange": "crawler_queue",
            "exchange_type": "direct",
            "routing_key": "crawler_queue"
        }
    }

)






