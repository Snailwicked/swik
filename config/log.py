# coding:utf-8
import os
import logging
import logging.config as log_conf
from config.conf import get_logging_args
args = get_logging_args()


log_dir = os.path.dirname(os.path.dirname(__file__))+args["log_dir"]
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

log_path = os.path.join(log_dir,args["log_name"])

log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'parser': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'other': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'storage': {
            'handlers': ['file'],
            'level': 'INFO',
        }
    }
}

log_conf.dictConfig(log_config)
other = logging.getLogger('other')
crawler = logging.getLogger('crawler')
parser = logging.getLogger('page_parser')
storage = logging.getLogger('storage')



def get_logger(name='aspider'):
    logging_format = "[%(asctime)s]-%(name)s-%(levelname)-6s"
    # logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(module)s::l%(lineno)d: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format,
        level=logging.DEBUG
    )
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("pyppeteer").setLevel(logging.INFO)
    logging.getLogger("websockets").setLevel(logging.INFO)
    return logging.getLogger(name)


__all__ = ['crawler', 'parser', 'other', 'storage']




