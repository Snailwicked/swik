# import requests
# import time
# import uuid
# import datetime
# import hmac
# import hashlib
# import json
# from algorithm.fakerspider.store import DbToMysql
# import asyncio
# from datetime import timedelta
#
#
# async def get_data():
#     await get_request()
#
#
# async def get_request():
#     # 十三位时间戳
#     current_time = str(round(time.time() * 1000))
#     create_time_f = datetime.datetime.now()
#     create_time = create_time_f - timedelta(minutes=30)
#     create_time = create_time.strftime('%Y-%m-%d %H:%M')
#     # 随机字符串
#     nonce = str(uuid.uuid3(uuid.NAMESPACE_DNS, create_time))
#     secret = 'qz7tt08ae3q7rouu9xvtkjbo7upk36qx'
#     hmac_key = secret + current_time + nonce
#     body_temp = {
#     "ds": create_time.replace('-', '').replace(':', '').replace(' ', ''),
#     "hh": "1",
#     "mi": "1"
#                }
#     # body_temp = {
#     #     "ds": "201906121725",
#     #     "hh": "1",
#     #     "mi": "1"
#     # }
#     body = json.dumps(body_temp)
#     sign = hmac.new(hmac_key.encode('utf-8'), body.encode('utf-8'), hashlib.md5).hexdigest()
#     url = 'https://secgw.alibaba.com/api/alisec.police.query.black.url?key=gjkd1fcnvkpc6pa2'
#     headers = {'time': current_time, 'nonce': nonce, 'sign': sign}
#     r = requests.post(url=url, headers=headers, data=body).text
#     r_dict = json.loads(r)
#     configs = {'host': '180.97.15.181', 'user': 'root', 'password': 'Vrv123!@#', 'db': 'fakespider'}
#     domain_set = set()
#     for i in r_dict['data']:
#         for k, value in i.items():
#             domain_set.add(value)
#     for domain in domain_set:
#         data = {'domain': domain, 'source_number': '1', 'crawl_time': create_time, 'isPass': '0'}
#         dbtm = DbToMysql(configs)
#         dbtm.save_one_data('wa_key', data)
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     task = loop.create_task(get_data())
#     loop.run_until_complete(task)


# class People:
#     def __init__(self, score):
#         self._score = score
#
#     @property
#     def score(self):
#         return self._score
#
#     @score.setter
#     def score(self, val):
#         if val < 0:
#             self._score = 0
#         elif val > 100:
#             self._score = 100
#         else:
#             self._score = val
#
#
# p = People(1)
# p.score = 101
# print(p.score)

