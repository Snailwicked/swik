import xlrd
import time
import time,hashlib
from pykafka import KafkaClient
from kafka import KafkaProducer

import json
data = {'id': '002dfeeb2fbe0bbcac398bae7c77c4bc', 'title': 'Automated Penetration Testing Startup Pcysys Raises $10 Million', 'content': 'Israeli cybersecurity firm Pcysys announced on Wednesday that it has completed a $10 million Series A funding round, which brings the total raised by the company to $15 million.Pcysys, an acronym for "Proactive Cyber Systems", offers an automated penetration testing platform that uses algorithms to scan and “ethically penetrate” corporate networks using various hacking techniques, and helps customers prioritize remediation efforts by identifying vulnerabilities that pose a higher risk.Founded in November 2015 by Arik Liberzon and Arik Faingold, the company says it has 50 employees and is approaching 100 paying enterprise customers.According to Pcysys CEO, Amitai Ratzon, the company plans to use the additional funding to expand its sales and support efforts in North America and EMEA and to further develop its enterprise technology.The Series A funding round was led by Canadian venture capital firm, Awz Ventures, along with investment giant Blackstone.', 'url': 'https://www.securityweek.com/automated-penetration-testing-startup-pcysys-raises-10-million', 'domain': '', 'poTime': 1573694554000, 'poMonth': 0, 'poDay': 0, 'poHour': 0, 'author': '', 'source': '网络安全时讯(securityweek)', 'addTime': 1573694554000, 'view': 0, 'replay': 0, 'pr': 0, 'administrativeId': '', 'importanceDegree': -1, 'snapshotAddress': '', 'positiveOrNegative': 0, 'spreadValue': 0, 'opinionValue': 0, 'sensitiveValue': 0, 'moodValue': 0, 'webSite': '网络安全时讯(securityweek)', 'webSiteType': 0, 'address': '\t美国', 'img': 0, 'file': False, 'doc': '', 'uuid': 'TT_192.168.30.33_8888_1575363295860_1', 'titlePrint': '', 'titleContentPrint': '', 'suggest': '', 'rubbish': 0, 'updateFrequency': 0, 'provinceCode': 0, 'abroad': 0, 'analyzer': 'en'}

'''
数据库插入类
'''
from dateutil.parser import parse as date_parser

# client = KafkaClient(hosts='180.97.15.172:9092')
# topic = client.topics[b'bmj']
# with topic.get_sync_producer() as producer:
#     message = bytes(str(json.dumps(data)), encoding='utf-8')
#     producer.produce(message)
#     print(message)

# producer = topic.get_sync_producer()
# print(producer)
# message = bytes(str(json.dumps(data)), encoding='utf-8')
# print(message)
# producer.produce(message)
# print(data)



# producer = KafkaProducer(
#                             bootstrap_servers=['180.97.15.172:9092']
#                          )
# message = bytes(str(json.dumps(data)), encoding='utf-8')
#
# producer.send(b'bmj', message)
# print(message)
# producer.close()



# '''
# 读取excel
# '''
# hash = hashlib.md5()
#
# def get_thirteenTime():
#     import time
#     millis = int(round(time.time() * 1000))
#     return millis
#
# def get_uuid():
#     def get_host_ip():
#         try:
#             import socket
#             s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             s.connect(('8.8.8.8', 80))
#             ip = s.getsockname()[0]
#         finally:
#             s.close()
#         return ip
#
#     struuid = "TT_{0}_8888_{1}_1".format(get_host_ip(), get_thirteenTime())
#     return struuid
#
# file = 'excel_data29.xls'
# import uuid
# def read_excel():
#     data = {}
#     wb = xlrd.open_workbook(filename=file)#打开文件
#     sheet1 = wb.sheet_by_index(0)
#     rows_num = sheet1.nrows
#     print(rows_num)
#     # with topic.get_sync_producer() as producer:
#     for i in range(2,rows_num):
#         hash.update(bytes(sheet1.cell_value(i, 3).replace("'","").replace("\n",""), encoding='utf-8'))
#         data["id"] = hash.hexdigest()
#         data["title"] = str(sheet1.cell_value(i, 0)).replace("'","").replace("\n","")
#         data["content"] = sheet1.cell_value(i, 7).replace("'","").replace("\n","")
#         data["url"] = sheet1.cell_value(i, 3).replace("'","").replace("\n","")
#         data["domain"] = ""
#         data["poTime"] =int(time.mktime(date_parser(str(sheet1.cell_value(i, 9)).replace("\\n", "").replace("\\t", "")).timetuple()))*1000
#         data["poMonth"]= 0
#         data["poDay"]= 0
#         data["poHour"]= 0
#         data["author"]= ""
#         data["source"]= sheet1.cell_value(i, 4).replace("'","").replace("\n","")
#         data["addTime"]= int(time.mktime(date_parser(str(sheet1.cell_value(i, 9)).replace("\\n", "").replace("\\t", "")).timetuple()))*1000
#         data["view"]= 0
#         data["replay"]= 0
#         data["pr"]= 0
#         data["administrativeId"]= ""
#         data["importanceDegree"]= -1
#         data["snapshotAddress"]= ""
#         data["positiveOrNegative"]= 0
#         data["spreadValue"]= 0
#         data["opinionValue"]= 0
#         data["sensitiveValue"]= 0
#         data["moodValue"]= 0
#         data["webSite"]= sheet1.cell_value(i, 4).replace("'","").replace("\n","")
#         data["webSiteType"]= 0
#         data["address"]= sheet1.cell_value(i, 2).replace("'","").replace("\n","")
#         data["img"]= 0
#         data["file"]= False
#         data["doc"]= ""
#         data["uuid"]= get_uuid()
#         data["titlePrint"]= ""
#         data["titleContentPrint"]= ""
#         data["suggest"]= ""
#         data["rubbish"]= 0
#         data["updateFrequency"]= 0
#         data["provinceCode"]= 0
#         data["abroad"]= 0
#         data["analyzer"]= "en"
#         message = bytes(str(json.dumps(data)), encoding='utf-8')
#         producer.produce(message)
#         print(data)
#
# read_excel()
