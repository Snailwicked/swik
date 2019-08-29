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

'''
   logging_format = "[%(asctime)s]-%(name)s-%(levelname)-6s"
    # logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(module)s::l%(lineno)d: "
    logging_format += "%(message)s"

'''
log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s-%(levelname)s - %(module)s ->%(lineno)d ; %(message)s',
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
        'crawler_info': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'crawler_debug': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },

        'web_info': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
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
other_info = logging.getLogger('other')
crawler_info = logging.getLogger('crawler_info')
crawler_debug = logging.getLogger('crawler_debug')
web_info = logging.getLogger('web_info')

parser_info = logging.getLogger('page_parser')
storage_info = logging.getLogger('storage')


__all__ = ['other_info', 'crawler_info', 'parser_info', 'storage_info',"crawler_debug","web_info"]




