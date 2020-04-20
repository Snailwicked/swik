# import requests
# from multiprocessing.dummy import Pool as ThreadPool
# import json
# import pymysql
# import datetime
# import re
# from datetime import timedelta
# from algorithm.fakerspider.tools import check_text, remove_emoji, get_domain
# from utils.headers import random_headers as headers
# import time
# import random
# import logging
# from algorithm.fakerspider.tools import get_number,parse_content
#
# db = pymysql.connect(host='180.97.15.181', port=3306, user='root', passwd='Vrv123!@#', db='fakespider',
#                      use_unicode=True, charset='utf8mb4')
# cursors = db.cursor()
# '''
# 多线程爬取微博上反诈骗中心需要的信息(根据关键词如"刷单","淘宝信誉","银行卡","代办信用卡","返现","返利"搜索)
#
# '''
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# def info_list(url):
#     '''
#     :param url:
#     :return: 信息列表
#     '''
#     try:
#         time.sleep(random.random())
#         r = requests.get(url=url, headers=headers, timeout=1.5)
#         resp = r.text
#     except Exception as e:
#         logger.error(e, url)
#     if resp:
#         results = json.loads(resp)
#         if results["ok"] == 1:
#             info_list_temp = results["data"]["cards"]
#             # 个别page会没有内容要判断处理下
#             if not info_list_temp:
#                 yield from []
#             else:
#                 info_list = info_list_temp[-1]["card_group"]
#                 yield from info_list
#
# def parse_info_list(item):
#     data = {}
#     data["isPass"] = 2
#     data["source"] = "新浪微博-重点网站"
#
#     account_id = item["user"]["id"]  # 账号id
#     account_nickname = item["user"]["screen_name"]  # 个人账号昵称
#     account_nickname = remove_emoji(account_nickname)
#     data["account_nickname"] = account_nickname
#
#     account_url = item["user"]["profile_url"]  # 个人账号主页地址
#     data["account_url"] = account_url
#
#     description_temp = item["desc1"].strip().replace(' ', '')  # 个人简介
#     # 这里的description_temp是因为有的没有简介,没有的抓到了粉丝数,这边加个判断去掉
#     if "粉丝" in description_temp:
#         description = ""
#     else:
#         description = description_temp
#         description = remove_emoji(description)
#     data["description"] = description
#
#     #     # 从用户列表接口返回的数据中得到了uid,去请求个人主页接口取微博内容,和
#     #     # 每个内容里的评论数,有就采,没有就不采
#     account_first_url = "https://m.weibo.cn/api/container/getIndex"
#     data["account_first_url"] = account_first_url
#     data["account_id"] = "account_id"
#     params = {
#         "type": "uid",
#         "value": str(account_id),
#         "containerid": "107603" + str(account_id),
#     }
#     data["params"] = params
#     return data
#
#
# def weibo_crawl(url):
#     for item in info_list(url):
#         result = parse_info_list(item)
#         print(result)
#         try:
#             time.sleep(random.random())
#             res = requests.get(url=result["account_first_url"], headers=headers, params=result["params"], timeout=2)
#         except Exception as e:
#             logger.error(e, url)
#         if res.text:
#             print(res.text)
#             res_dict = json.loads(res.text)
#             if res_dict["ok"] == 1:
#                 if "cardlistInfo" in res_dict["data"]:
#                     total = res_dict["data"]["cardlistInfo"]["total"]
#                     max_page = int(total / 10 + 1)
#                     for k in range(1, max_page + 1):
#                         account_api = "https://m.weibo.cn/api/container/getIndex"
#                         querystring = {
#                             "type": "uid",
#                             "value": str(result["account_id"]),
#                             "containerid": "107603" + str(result["account_id"]),
#                             "page": str(k)
#                         }
#                         try:
#                             time.sleep(random.random())
#                             r = requests.get(url=account_api, headers=headers, params=querystring, timeout=2.5)
#                         except Exception as e:
#                             logger.error(e, url)
#                         if r.status_code == 200:
#                             res = r.text
#                             if res:
#                                 results = json.loads(res)
#                                 if results["ok"] == 1:
#
#                                 if "cards" in results["data"]:
#                                     comments_temp_counts = results["data"]["cards"]
#                                     for item in comments_temp_counts:
#                                         if "mblog" in item:
#                                             content_temp = item["mblog"]["text"]
#                                             pattern = re.compile(r'<[^>]+>')  # 正则去掉标签内容
#                                             content = pattern.sub('', content_temp).replace('&quot', '')  # 微博正文
#                                             content = remove_emoji(content)
#                                             publish_time_temp = item["mblog"]["created_at"]  # 微博正文发布时间
#                                             if len(publish_time_temp) < 6:
#                                                 if "前" in publish_time_temp:
#                                                     publish_time = datetime.datetime.today().strftime(
#                                                         '%Y-%m-%d')
#                                                 elif "刚刚" in publish_time_temp:
#                                                     publish_time = datetime.datetime.today().strftime('%Y-%m-%d')
#                                                 else:
#                                                     now_year_temp = datetime.datetime.today()
#                                                     now_year = datetime.datetime.strftime(now_year_temp, "%Y-")
#                                                     publish_time = now_year + publish_time_temp
#                                             else:
#                                                 if "昨天" in publish_time_temp:
#                                                     tday = datetime.datetime.today()
#                                                     wday = tday - datetime.timedelta(days = 1)
#                                                     publish_time = datetime.datetime.strftime(wday, '%Y-%m-%d')
#                                                 else:
#                                                     publish_time = publish_time_temp
#                                             crawl_time = datetime.datetime.today().strftime(
#                                                 '%Y-%m-%d %H:%M:%S')  # 爬取时间
#                                             comments_count = item["mblog"][
#                                                 "comments_count"]  # 根据评论数是否为零去爬评论
#                                             mid = item["mblog"][
#                                                 "id"]  # mid和id是获取评论第一条接口的主要参数,后面的评论还需要另外一个max_id
#                                             if comments_count == 0:
#                                                 comments = ""
#                                                 comments_nickname = ""
#                                                 if account_nickname == None:
#                                                     account_nickname = ""
#                                                 if description == None:
#                                                     description = ""
#                                                 if content == None:
#                                                     content = ""
#                                                 text = description.strip() + " " + content.strip() +" " + comments.strip() + " "
#                                                 if check_text(text):
#                                                     if "博彩"  not in url:
#                                                         domain = ""
#
#                                                     domain, e_mail, website, weixin, weixinhao, qq, qq_detail, phone, phone_detail = get_number(
#                                                         text)
#
#                                                     try:
#                                                         # 先查有没有有效信息,再查有效信息在不在库里,不在则入库
#                                                         if weixinhao or qq or phone or domain:
#                                                             sql = 'SELECT DISTINCT weixinhao, qq, phone, domain FROM wa_key where source="%s"' % source
#                                                             cursors.execute(sql)
#                                                             db.commit()
#                                                             results = set(cursors.fetchall())
#                                                             if (weixinhao, qq, phone, domain) not in results:
#                                                                 sql = 'insert into wa_key(source, account_url, account_nickname, description, content, comments, crawl_time, publish_time, comments_nickname, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, domain, source_number) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d")' % (
#                                                                 source, account_url,
#                                                                 pymysql.escape_string(account_nickname), pymysql.escape_string(description),
#                                                                 pymysql.escape_string(content), pymysql.escape_string(comments), crawl_time,
#                                                                 publish_time, comments_nickname, isPass, weixin, weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone, e_mail, domain, 2)
#                                                                 cursors.execute(sql)
#                                                                 db.commit()
#                                                     except Exception as e:
#                                                         logger.error(e)
#                                                         db.rollback()
# #
# #                                             else:
# #                                                 # 去爬评论接口,这里注意下headers里的referer要改下,不然没数据
# #                                                 comments_first_api = "https://m.weibo.cn/comments/hotflow"
# #                                                 new_headers = {
# #                                                     'Accept': 'application/json, text/plain, */*',
# #                                                     'Accept-Encoding': 'gzip, deflate, br',
# #                                                     'Accept-Language': 'zh-CN,zh;q=0.9',
# #                                                     'Connection': 'keep-alive',
# #                                                     'Host': 'm.weibo.cn',
# #                                                     'MWeibo-Pwa': '1',
# #                                                     'Referer': 'https://m.weibo.cn/status/' + mid,
# #                                                     'User-Agent': 'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
# #                                                     'X-Requested-With': 'XMLHttpRequest',
# #                                                 }
# #                                                 params = {"id": mid, "mid": mid, "max_id_type": "0"}
# #                                                 # time.sleep(random.random())
# #                                                 try:
# #                                                     time.sleep(random.random())
# #                                                     r = requests.get(url=comments_first_api,
# #                                                                      headers=new_headers, params=params,
# #                                                                      timeout=3)
# #                                                 except Exception as e:
# #                                                     logger.error(e, url)
# #                                                 if r.status_code == 200:
# #                                                     reps = json.loads(r.text)
# #                                                     if reps:
# #                                                         if "data" in reps:
# #                                                             comments_info_list = reps["data"][
# #                                                                 "data"]  # comments_info是个评论信息列表里面有评论内容和评论人评论时间等
# #                                                             for comments_info in comments_info_list:
# #                                                                 comments_temp = comments_info["text"]
# #                                                                 pattern = re.compile(
# #                                                                     r'<[^>]+>')  # 微博表情是span标签内的,去除无用的表情标签
# #                                                                 comments = pattern.sub('',
# #                                                                                        comments_temp).replace(
# #                                                                     '&quot', '')  # 评论内容
# #                                                                 comments = remove_emoji(comments)
# #                                                                 # comments_time = comments_info["created_at"]
# #                                                                 comments_nickname = \
# #                                                                 comments_info["user"][
# #                                                                     "screen_name"]  # 评论人昵称
# #                                                                 comments_nickname = remove_emoji(comments_nickname)
# #                                                                 if account_nickname == None:
# #                                                                     account_nickname = ""
# #                                                                 if description == None:
# #                                                                     description = ""
# #                                                                 if content == None:
# #                                                                     content = ""
# #                                                                 if comments == None:
# #                                                                     comments = ""
# #                                                                 if comments_nickname == None:
# #                                                                     comments_nickname = ""
# #                                                                 text = description.strip() + " " + content.strip() + " " + comments.strip() + " "
# #                                                                 if check_text(text):
# #                                                                     if "博彩" not in url:
# #                                                                         domain = ""
# #                                                                     domain, e_mail, website, weixin, weixinhao, qq, qq_detail, phone, phone_detail = get_number(
# #                                                                         text)
# #                                                                     try:
# #                                                                         # 先查有没有有效信息,再查有效信息在不在库里,不在则入库
# #                                                                         if weixinhao or qq or phone or domain:
# #                                                                             sql = 'SELECT DISTINCT weixinhao, qq, phone, domain FROM wa_key where source="%s"' % source
# #                                                                             cursors.execute(sql)
# #                                                                             db.commit()
# #                                                                             results = set(cursors.fetchall())
# #                                                                             if (weixinhao, qq, phone, domain) not in results:
# #                                                                                 sql = 'insert into wa_key(source, account_url, account_nickname, description, content, comments, crawl_time, publish_time, comments_nickname, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, domain, source_number) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d")' % (
# #                                                                                 source, account_url,
# #                                                                                 account_nickname, description,
# #                                                                                 content, comments, crawl_time,
# #                                                                                 publish_time, comments_nickname, isPass, weixin, weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone, e_mail, domain, 2)
# #                                                                                 cursors.execute(sql)
# #                                                                                 db.commit()
# #                                                                     except Exception as e:
# #                                                                         logger.error(e)
# #                                                                         db.rollback()
# # db.close()
# # except Exception as e:
# # logger.error(e)
#
#
# if __name__ == '__main__':
#     url_list = []
#     url_sd_list = []
#     url_tbxy_list = []
#     url_yhk_list = []
#     url_dbxyk_list = []
#     url_fx_list = []
#     url_fl_list = []
#     url_sycz_list = []
#     url_bc_list = []
#     for i in range(1, 2):
#         # url_tbxy = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%26t%3D0&page_type=searchall&page={}'.format(
#         #     i)
#         # url_tbxy_list.append(url_tbxy)
#         # url_sd = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E5%88%B7%E5%8D%95%26t%3D0&page_type=searchall&page={}'.format(
#         #     i)
#         # url_sd_list.append(url_sd)
#         # url_dbxyk = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E4%BB%A3%E5%8A%9E%E4%BF%A1%E7%94%A8%E5%8D%A1%26t%3D0&page_type=searchall&page={}'.format(
#         #     i)
#         # url_dbxyk_list.append(url_dbxyk)
#         # url_yhk = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E9%93%B6%E8%A1%8C%E5%8D%A1%26t%3D0&page_type=searchall&page={}'.format(
#         #     i)
#         # url_yhk_list.append(url_yhk)
#         # url_fx = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E8%BF%94%E7%8E%B0%26t%3D0&page_type=searchall&page={}'.format(
#         #     i)
#         # url_fx_list.append(url_fx)
#         # url_fl = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E8%BF%94%E5%88%A9%26t%3D0&page_type=searchall&page={}'.format(
#         #     i)
#         # url_fl_list.append(url_fl)
#         # url_sycz = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E6%89%8B%E6%B8%B8%E5%85%85%E5%80%BC%26t%3D0&page_type=searchall&page={}'.format(
#         #     i)
#         # url_sycz_list.append(url_sycz)
#         url_bc = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E5%8D%9A%E5%BD%A9%26t%3D0&page_type=searchall&page={}'.format(i)
#         url_bc_list.append(url_bc)
#     url_list.extend(url_sd_list)
#     url_list.extend(url_tbxy_list)
#     url_list.extend(url_dbxyk_list)
#     url_list.extend(url_yhk_list)
#     url_list.extend(url_fl_list)
#     url_list.extend(url_fx_list)
#     url_list.extend(url_sycz_list)
#     url_list.extend(url_bc_list)
#     random.shuffle(url_list)
#     pool = ThreadPool(8)
#     pool.map(weibo_crawl, url_list)
#     pool.close()
#     pool.join()
