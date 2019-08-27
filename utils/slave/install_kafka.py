# from SQL_DB.db.redisclient import RedisClient
# from slave.newsinfoutil import parseUrl
# from pykafka import KafkaClient
# import logging.config ,json ,time
# from SQL_DB.config.config import Config
#
# logger_conf = Config().get_logger_args()
# logging.config.dictConfig(logger_conf)
#
# class Redis_spider(object):
#
#     def __init__(self):
#         self.redis_batch_size = 16
#         self.redis_encoding = "utf-8"
#         self.server = RedisClient()
#         self.requests_redis_key = "request_url"
#         self.error_redis_key = "error_url"
#         self.client = KafkaClient(hosts='192.168.30.91:9092,192.168.30.113:9092,192.168.30.114:9092/kafka')
#         self.topic = self.client.topics[b'document']
#
#     def slave_spider(self):
#
#         while 1:
#             data = self.server.get_urlFromhead(self.requests_redis_key)
#             if not data:
#                 break
#             if data:
#                 yield data
#
#     def parse_Url(self):
#         with self.topic.get_sync_producer() as producer:
#             for url in self.slave_spider():
#                 test = bytes.decode(url[1])
#
#                 newsinfo = ""
#                 try:
#                     parse_url = parseUrl(url=test)
#                     urldata = parse_url.get_info()
#                     if urldata["snapshotAddress"] == "":
#                         newsinfo = ""
#                     newsinfo = urldata
#                 except Exception as e:
#                     tests = []
#                     tests.append(test)
#                     self.server.add_urls(self.error_redis_key, tests)
#                     logging.error("解析异常<{0}>，{1}".format(test, e))
#
#
#                 if newsinfo != "":
#                     try:
#                         string = bytes(str(json.dumps(newsinfo)), encoding='utf-8')
#                         producer.produce(string)
#                         print(newsinfo)
#                         time.sleep(0.01)
#                     except Exception as e:
#                         logging.error("插入失败<{1}>，{0}".format(newsinfo, e))
#
#
#
#
