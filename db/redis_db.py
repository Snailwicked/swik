import json
import redis
from config.conf import get_redis_args
REDIS_ARGS = get_redis_args()
urls_db = REDIS_ARGS.get('urls', 2)
host = REDIS_ARGS.get('host', '127.0.0.1')
port = REDIS_ARGS.get('port', 6379)
urls_con = redis.Redis(host=host, port=port,db=urls_db)


class Url_Parameter(object):
    @classmethod
    def store_parameter(cls, spider_name, parameter):
        urls_con.rpush(spider_name, json.dumps(parameter))


    @classmethod
    def fetch_parameters(cls,spider_name):
        parameters = urls_con.lrange(spider_name,1,20)
        urls_con.ltrim(spider_name,20,-1)
        return parameters

    @classmethod
    def fetch_llen(cls, spider_name):
        parameters = urls_con.llen(spider_name)
        return parameters

class Clear_Con():

    def clear(self):
        broker = REDIS_ARGS.get('broker', 7)
        urls_con = redis.Redis(host=host, port=port,db=broker)
        for elem in urls_con.keys():
            urls_con.delete(elem)
if __name__ == '__main__':
    clear_con = Clear_Con()
    clear_con.clear()