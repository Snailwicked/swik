# coding:utf-8
import os
import random
from yaml import load,FullLoader

config_path = os.path.join(os.path.dirname(__file__), 'spider.yaml')

with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf =load(cont, Loader=FullLoader)

def get_db_args():
    return cf.get('db')


def get_algorithm():
    return cf.get('algorithm')

def get_redis_args():
    return cf.get('redis')


def get_timeout():
    return cf.get('time_out')


def get_crawl_interal():
    interal = random.randint(cf.get('min_crawl_interal'), cf.get('max_crawl_interal'))
    return interal


def get_excp_interal():
    return cf.get('excp_interal')


def get_max_repost_page():
    return cf.get('max_repost_page')


def get_max_search_page():
    return cf.get('max_search_page')


def get_max_home_page():
    return cf.get('max_home_page')


def get_max_comment_page():
    return cf.get('max_comment_page')


def get_max_retries():
    return cf.get('max_retries')


def get_broker_and_backend():
    redis_info = cf.get('redis')
    password = redis_info.get('password')
    db = redis_info.get('broker', 5)
    host = redis_info.get('host')
    port = redis_info.get('port')
    backend_db = redis_info.get('backend', 6)
    broker_url = 'redis://{}:{}/{}'.format(host, port, db)
    backend_url = 'redis://{}:{}/{}'.format(host, port, backend_db)
    return broker_url, backend_url


def get_redis_master():
    return cf.get('redis').get('master', '')


def get_code_username():
    return cf.get('yundama_username')

def get_code_password():
    return cf.get('yundama_passwd')

def get_email_args():
    return cf.get('email')

def get_logging_args():
    return cf.get('logging')


def get_mongo_args():
    return cf.get('mongo')