# -*- coding: utf-8 -*-
# from slave.newsinfoutil import parseUrl
from pykafka import KafkaClient
import logging.config ,json ,time
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


data = {
"id": "65ba46a9c488e4a6c290b693b1b60731",
"title": "科任如何上好第一节课",
"content": "　　<br />　　本人是一位男老师，不过也是失败的教育者。为什么说呢？因为第一学期第一节课后课堂纪律乱糟糟，几乎无法掌控，这样子想学习的也学不了，几乎不把老师放在眼里，就更谈不上尊重了，自然成绩肯定好不到哪里去，每天情绪非常低落，一个男孩子现在却是保持在100斤，瘦的可怕。<br />　　<br />　　借天涯平台我想请教一下同行，科任老师如何上好第一节课，特别是如何在第一节课给学生下马威，如何保持课堂秩序和纪律？使学生又怕又敬你？好像我接触陌生班，第一节课师生有点陌生，所以课堂纪律还过得去，可是以后的话课堂纪律是越来越糟，自己过得很痛苦。特别是自修课（我这是一个乡镇农村中学）第一节课还好掌控，可是到第二节就开始松动了，然后接着以后就越来越控制不了课堂纪律了。<br />　　<br />　　所以在这里我想请教大家，第一节正课和自修课学生出现违纪，比如讲话，有位，玩东西的如何处罚比较合理，使得学生后怕，以后上课纪律顺风顺水？哟就是第一节学生出现讲话走位玩东西的没有拿出合理的处理方法，影响以后学生都不怕我了。<br />　　<br />　　我个人性格特内向，然后又懒得处罚学生，几乎学生违纪拿不出更好的制裁方法，久而久之，以后课堂失去掌控，每天过得都很痛苦，看到其他老师上课那么自由轻松，我真的想辞职的不干，可是自己又没其他能耐，假如失去这份工作，其他路真的好走吗？<br />　　<br />　　真是正处于痛苦中，希望同仁指点迷津一二，感激不尽，谢谢！<br />　　<br />　　<br />　　<br />　　<br />人打赏<br />0 人 点赞",
"url": "http://bbs.tianya.cn/post-140-649560-1.shtml",
"poTime": 1536076800000,
"poMonth": 201809,
"poDay": 20180905,
"poHour": 2018090500,
"domain": "tianya.cn",
"author": "情结千千",
"source": "",
"addTime": 1570539950502,
"pr": 0,
"webSiteType": 1,
"webSite": "天涯论坛-教师",
"positiveOrNegative": 2,
"abroad": 0,
"spreadValue": -47,
"replay": 2,
"view": 154,
"importanceDegree": -1,
"opinionValue": 248,
"sensitiveValue": -11656,
"snapshotAddress": "",
"administrativeId": "000000",
"titlePrint": "28d6a48d2ee56e0add83cec71fe5c224",
"titleContentPrint": "8baf847d87dc2c35df029151a1166835",
"img": "",
"moodValue": 65336,
"uuid": "TT_192.168.10.10_28135_1541493719209_1",
"updateFrequency": 0,
"suggest": "　　",
"rubbish": 0,
"importantValue": 0,
"provinceCode": 0
}


# from kafka import KafkaProducer
# import json
#
# '''
#     生产者demo
#     向test_lyl2主题中循环写入10条json数据
#     注意事项：要写入json数据需加上value_serializer参数，如下代码
# '''
# producer = KafkaProducer(
#     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#     bootstrap_servers=['180.97.15.172:9092', '180.97.15.173:9092', '180.97.15.174:9092']
# )
# for i in range(10):
#     data = {
#         "name": "李四",
#         "age": 23,
#         "gender": "男",
#         "id": i
#     }
#     producer.send('document', data,partition=0)
# producer.close()