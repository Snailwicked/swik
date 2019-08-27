import requests
from multiprocessing.dummy import Pool as ThreadPool
import json
import pymysql
import datetime
import re
from datetime import timedelta
from algorithm.fakerspider.tools import check_text, remove_emoji, get_domain
from pypinyin import lazy_pinyin
import time
import random
import logging


'''
多线程爬取微博上反诈骗中心需要的信息(根据关键词如"刷单","淘宝信誉","银行卡","代办信用卡","返现","返利"搜索)

'''
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'm.weibo.cn',
    'MWeibo-Pwa': '1',
    'Referer': 'https://m.weibo.cn/p/searchall?containerid=100103type%3D1%26q%3D%E6%B7%98%E5%AE%9D%E5%88%B7%E5%8D%95',
    'User-Agent': random.choice(USER_AGENTS),
    'X-Requested-With': 'XMLHttpRequest',
}


def weibo_crawl(url):
    # try:
        # db = pymysql.connect(host='180.97.15.181', port=3306, user='root', passwd='Vrv123!@#', db='fakespider', use_unicode=True, charset='utf8mb4')
        # cursors = db.cursor()
    try:
        time.sleep(random.random(4))
        r = requests.get(url=url, headers=headers, timeout=1.5)
        resp = r.text
        print(resp)
    except Exception as e:
        logger.error(e, url)
    #     if resp:
    #         results = json.loads(resp)
    #         if results["ok"] == 1:
    #             info_list_temp = results["data"]["cards"]
    #             # 个别page会没有内容要判断处理下
    #             if not info_list_temp:
    #                 pass
    #             else:
    #                 info_list = info_list_temp[-1]["card_group"]
    #                 for info in info_list:
    #                     isPass = 2
    #                     source = "新浪微博-重点网站"
    #                     account_id = info["user"]["id"]  # 账号id
    #                     account_nickname = info["user"]["screen_name"]  # 个人账号昵称
    #                     account_nickname = remove_emoji(account_nickname)
    #                     account_url = info["user"]["profile_url"]  # 个人账号主页地址
    #                     description_temp = info["desc1"].strip().replace(' ', '')  # 个人简介
    #                     # 这里的description_temp是因为有的没有简介,没有的抓到了粉丝数,这边加个判断去掉
    #                     if "粉丝" in description_temp:
    #                         description = ""
    #                     else:
    #                         description = description_temp
    #                         description = remove_emoji(description)
    #                     # 从用户列表接口返回的数据中得到了uid,去请求个人主页接口取微博内容,和
    #                     # 每个内容里的评论数,有就采,没有就不采
    #                     account_first_url = "https://m.weibo.cn/api/container/getIndex"
    #                     params = {
    #                         "type": "uid",
    #                         "value": str(account_id),
    #                         "containerid": "107603" + str(account_id),
    #                     }
    #                     try:
    #                         time.sleep(random.random())
    #                         res = requests.get(url=account_first_url, headers=headers, params=params, timeout=2)
    #                     except Exception as e:
    #                         logger.error(e, url)
    #                     if res.text:
    #                         res_dict = json.loads(res.text)
    #                         if res_dict["ok"] == 1:
    #                             if "cardlistInfo" in res_dict["data"]:
    #                                 total = res_dict["data"]["cardlistInfo"]["total"]
    #                                 max_page = int(total / 10 + 1)
    #                                 for k in range(1, max_page + 1):
    #                                     account_api = "https://m.weibo.cn/api/container/getIndex"
    #                                     querystring = {
    #                                         "type": "uid",
    #                                         "value": str(account_id),
    #                                         "containerid": "107603" + str(account_id),
    #                                         "page": str(k)
    #                                     }
    #                                     try:
    #                                         time.sleep(random.random())
    #                                         r = requests.get(url=account_api, headers=headers, params=querystring, timeout=2.5)
    #                                     except Exception as e:
    #                                         logger.error(e, url)
    #                                     if r.status_code == 200:
    #                                         res = r.text
    #                                         if res:
    #                                             results = json.loads(res)
    #                                             if results["ok"] == 1:
    #                                                 if "cards" in results["data"]:
    #                                                     comments_temp_counts = results["data"]["cards"]
    #                                                     for item in comments_temp_counts:
    #                                                         if "mblog" in item:
    #                                                             content_temp = item["mblog"]["text"]
    #                                                             pattern = re.compile(r'<[^>]+>')  # 正则去掉标签内容
    #                                                             content = pattern.sub('', content_temp).replace('&quot', '')  # 微博正文
    #                                                             content = remove_emoji(content)
    #                                                             publish_time_temp = item["mblog"]["created_at"]  # 微博正文发布时间
    #                                                             if len(publish_time_temp) < 6:
    #                                                                 if "前" in publish_time_temp:
    #                                                                     publish_time = datetime.datetime.today().strftime(
    #                                                                         '%Y-%m-%d')
    #                                                                 elif "刚刚" in publish_time_temp:
    #                                                                     publish_time = datetime.datetime.today().strftime('%Y-%m-%d')
    #                                                                 else:
    #                                                                     now_year_temp = datetime.datetime.today()
    #                                                                     now_year = datetime.datetime.strftime(now_year_temp, "%Y-")
    #                                                                     publish_time = now_year + publish_time_temp
    #                                                             else:
    #                                                                 if "昨天" in publish_time_temp:
    #                                                                     tday = datetime.datetime.today()
    #                                                                     wday = tday - datetime.timedelta(days = 1)
    #                                                                     publish_time = datetime.datetime.strftime(wday, '%Y-%m-%d')
    #                                                                 else:
    #                                                                     publish_time = publish_time_temp
    #                                                             crawl_time = datetime.datetime.today().strftime(
    #                                                                 '%Y-%m-%d %H:%M:%S')  # 爬取时间
    #                                                             comments_count = item["mblog"][
    #                                                                 "comments_count"]  # 根据评论数是否为零去爬评论
    #                                                             mid = item["mblog"][
    #                                                                 "id"]  # mid和id是获取评论第一条接口的主要参数,后面的评论还需要另外一个max_id
    #                                                             if comments_count == 0:
    #                                                                 comments = ""
    #                                                                 comments_nickname = ""
    #                                                                 if account_nickname == None:
    #                                                                     account_nickname = ""
    #                                                                 if description == None:
    #                                                                     description = ""
    #                                                                 if content == None:
    #                                                                     content = ""
    #                                                                 text = description.strip() + " " + content.strip() +" " + comments.strip() + " "
    #                                                                 if check_text(text):
    #                                                                     if "博彩" in url:
    #                                                                         domain = re.search(r'(https?://)?([\da-z-]+)\.([\da-z\.-]*)[\.]*([a-z\.]{2,6})([/a-zA-Z0-9\.-]+)+/?', text)
    #                                                                         if domain:
    #                                                                             domain = domain[0]
    #                                                                             if "www" in domain:
    #                                                                                 domain = get_domain(domain)
    #                                                                             elif ".." in domain:
    #                                                                                 domain = ""
    #                                                                             else:
    #                                                                                 domain = domain
    #                                                                         else:
    #                                                                             domain = ""
    #                                                                     else:
    #                                                                         domain = ""
    #                                                                     phone_detail = re.findall(r'[\D]{0,7}[\D]{1}1[35789]\d{9,}', text)
    #                                                                     phone_set = set()
    #                                                                     phone = ""
    #                                                                     if len(phone_detail) > 0:
    #                                                                         phone_detail = phone_detail[0]
    #                                                                         phone = re.findall(r'1[35789]\d{9,}', phone_detail)
    #                                                                         if len(phone) > 0:
    #                                                                             phone = phone[0]
    #                                                                         else:
    #                                                                             phone_detail = ""
    #                                                                             phone = ""
    #                                                                     else:
    #                                                                         phone_detail = ""
    #                                                                         phone = ""
    #                                                                     qq_detail = re.findall(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', text)
    #                                                                     if len(qq_detail)>0:
    #                                                                         qq_detail = qq_detail[0]
    #                                                                         qq = re.findall(r'[1-9][0-9]{4,14}', qq_detail)[0]
    #                                                                     else:
    #                                                                         qq_detail = ""
    #                                                                         qq = ""
    #                                                                     e_mail = re.findall(r'([a-zA-Z0-9_.+-]+@[a-fh-pr-zA-FH-PRZ0-9-]+\.[a-zA-Z0-9-.]+)', text)
    #                                                                     if len(e_mail) > 0:
    #                                                                         e_mail = e_mail[0]
    #                                                                     else:
    #                                                                         e_mail = ""
    #                                                                     text = re.sub(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', ' ', text)
    #                                                                     text = text.replace("，", " ").replace("。", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
    #                                                                     weixinhaos_set = set()
    #                                                                     weixinhao = ""
    #                                                                     weixin = re.findall(r'[\s\S]{0,3}[\u4E00-\u9FA5 | \u0041-u005A | \u0061-\u007A]{1,4}[\s\S]{0,5}[A-Za-z0-9_-]{6,22}[^\s]+', text)
    #                                                                     if len(weixin) > 0:
    #                                                                         weixin = weixin[0]
    #                                                                         weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
    #                                                                         weixin_cut = weixin.replace(weixinhao, "") + weixinhao[0:2]
    #                                                                         weixin_pinyin0 = lazy_pinyin(weixin_cut)
    #                                                                         weixin_pinyins0 = ""
    #                                                                         for j in weixin_pinyin0:
    #                                                                             j = j.lower()
    #                                                                             weixin_pinyins0 = weixin_pinyins0 + " " + j
    #                                                                         weixin_pinyins0 = weixin_pinyins0.replace(
    #                                                                             'nv', ' ').replace('lv', ' ').replace(
    #                                                                             'wei bo', ' ')
    #                                                                         if "❤" in weixin_pinyins0 or "v" in weixin_pinyins0 or "wei" in weixin_pinyins0 or "wx" in weixin_pinyins0 or "vx" in weixin_pinyins0 or "weix" in weixin_pinyins0 or "wei x" in weixin_pinyins0:
    #                                                                             weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
    #                                                                             if "vx" == weixinhao[:2].lower() or "wx" == weixinhao[:2].lower() and "wxid" != weixinhao[:4].lower():
    #                                                                                 weixinhao = weixinhao[2:]
    #                                                                             elif "v" == weixinhao[
    #                                                                                 0].lower() and re.match(
    #                                                                                 r'1[35789]\d{9,}', weixinhao[1:]):
    #                                                                                 weixinhao = weixinhao[1:]
    #                                                                             elif "wxid" == weixinhao[:4].lower():
    #                                                                                 if "_" == weixinhao[5]:
    #                                                                                     weixinhao = weixinhao
    #                                                                                 else:
    #                                                                                     weixinhao = weixinhao.replace(
    #                                                                                         weixinhao[4], "_")
    #                                                                             else:
    #                                                                                 weixinhao = weixinhao
    #                                                                         else:
    #                                                                             if "@" in weixin or "#" in weixin:
    #                                                                                 weixin = re.sub('[a-zA-Z]*v[a-zA-Z]*', ' ', weixin)
    #                                                                             if weixin != []:
    #                                                                                 weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)
    #                                                                                 if len(weixinhao) > 0:
    #                                                                                     weixinhao = weixinhao[0]
    #                                                                                     i_1 = weixin.replace(weixinhao,"")
    #                                                                                     i_1 = i_1.replace("加我", "wei").replace("+", "wei").replace("未", "").replace("为", "").replace("位","").replace("围","").replace("➕","wei").replace("喂","").replace("维","").replace("伟","").replace("唯","").replace("胃","").replace("卫","").replace("威","").replace("味","")
    #                                                                                     weixin_pinyin = lazy_pinyin(i_1)
    #                                                                                     weixin_pinyins = ""
    #                                                                                     for j in weixin_pinyin:
    #                                                                                         j = j.lower()
    #                                                                                         weixin_pinyins = weixin_pinyins + ' '+ j
    #                                                                                     i_2 = weixin_pinyins.replace("weibo", "").replace("nv", "").replace("lv", "").replace("wei bo", "")
    #                                                                                     if "v" in i_2 or "wei" in i_2:
    #                                                                                         weixin = weixin
    #                                                                                         if "vx" == weixinhao[
    #                                                                                                    -2:].lower():
    #                                                                                             weixinhao = weixinhao[
    #                                                                                                         :-2]
    #                                                                                         weixinhao = weixinhao
    #                                                                                     else:
    #                                                                                         weixin = ""
    #                                                                                         weixinhao = ""
    #                                                                                 else:
    #                                                                                     weixin = ""
    #                                                                                     weixinhao = ""
    #                                                                             else:
    #                                                                                 weixin = ""
    #                                                                                 weixinhao = ""
    #                                                                     else:
    #                                                                         weixin = ""
    #                                                                         weixinhao = ""
    #
    #                                                                     print(weixinhao ,qq ,phone ,domain)
    #                                                                     # try:
    #                                                                     #     # 先查有没有有效信息,再查有效信息在不在库里,不在则入库
    #                                                                     #     if weixinhao or qq or phone or domain:
    #                                                                     #         sql = 'SELECT DISTINCT weixinhao, qq, phone, domain FROM wa_key where source="%s"' % source
    #                                                                     #         cursors.execute(sql)
    #                                                                     #         db.commit()
    #                                                                     #         results = set(cursors.fetchall())
    #                                                                     #         if (weixinhao, qq, phone, domain) not in results:
    #                                                                     #             sql = 'insert into wa_key(source, account_url, account_nickname, description, content, comments, crawl_time, publish_time, comments_nickname, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, domain, source_number) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d")' % (
    #                                                                     #             source, account_url,
    #                                                                     #             pymysql.escape_string(account_nickname), pymysql.escape_string(description),
    #                                                                     #             pymysql.escape_string(content), pymysql.escape_string(comments), crawl_time,
    #                                                                     #             publish_time, comments_nickname, isPass, weixin, weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone, e_mail, domain, 2)
    #                                                                     #             cursors.execute(sql)
    #                                                                     #             db.commit()
    #                                                                     # except Exception as e:
    #                                                                     #     logger.error(e)
    #                                                                     #     db.rollback()
    #
    #                                                             else:
    #                                                                 # 去爬评论接口,这里注意下headers里的referer要改下,不然没数据
    #                                                                 comments_first_api = "https://m.weibo.cn/comments/hotflow"
    #                                                                 new_headers = {
    #                                                                     'Accept': 'application/json, text/plain, */*',
    #                                                                     'Accept-Encoding': 'gzip, deflate, br',
    #                                                                     'Accept-Language': 'zh-CN,zh;q=0.9',
    #                                                                     'Connection': 'keep-alive',
    #                                                                     'Host': 'm.weibo.cn',
    #                                                                     'MWeibo-Pwa': '1',
    #                                                                     'Referer': 'https://m.weibo.cn/status/' + mid,
    #                                                                     'User-Agent': 'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    #                                                                     'X-Requested-With': 'XMLHttpRequest',
    #                                                                 }
    #                                                                 params = {"id": mid, "mid": mid, "max_id_type": "0"}
    #                                                                 # time.sleep(random.random())
    #                                                                 try:
    #                                                                     time.sleep(random.random())
    #                                                                     r = requests.get(url=comments_first_api,
    #                                                                                      headers=new_headers, params=params,
    #                                                                                      timeout=3)
    #                                                                 except Exception as e:
    #                                                                     logger.error(e, url)
    #                                                                 if r.status_code == 200:
    #                                                                     reps = json.loads(r.text)
    #                                                                     if reps:
    #                                                                         if "data" in reps:
    #                                                                             comments_info_list = reps["data"][
    #                                                                                 "data"]  # comments_info是个评论信息列表里面有评论内容和评论人评论时间等
    #                                                                             for comments_info in comments_info_list:
    #                                                                                 comments_temp = comments_info["text"]
    #                                                                                 pattern = re.compile(
    #                                                                                     r'<[^>]+>')  # 微博表情是span标签内的,去除无用的表情标签
    #                                                                                 comments = pattern.sub('',
    #                                                                                                        comments_temp).replace(
    #                                                                                     '&quot', '')  # 评论内容
    #                                                                                 comments = remove_emoji(comments)
    #                                                                                 # comments_time = comments_info["created_at"]
    #                                                                                 comments_nickname = \
    #                                                                                 comments_info["user"][
    #                                                                                     "screen_name"]  # 评论人昵称
    #                                                                                 comments_nickname = remove_emoji(comments_nickname)
    #                                                                                 if account_nickname == None:
    #                                                                                     account_nickname = ""
    #                                                                                 if description == None:
    #                                                                                     description = ""
    #                                                                                 if content == None:
    #                                                                                     content = ""
    #                                                                                 if comments == None:
    #                                                                                     comments = ""
    #                                                                                 if comments_nickname == None:
    #                                                                                     comments_nickname = ""
    #                                                                                 text = description.strip() + " " + content.strip() + " " + comments.strip() + " "
    #                                                                                 if check_text(text):
    #                                                                                     if "博彩" in url:
    #                                                                                         domain = re.search(r'(https?://)?([\da-z-]+)\.([\da-z\.-]*)[\.]*([a-z\.]{2,6})([/a-zA-Z0-9\.-]+)+/?', text)
    #                                                                                         if domain:
    #                                                                                             domain = domain[0]
    #                                                                                             if "www" in domain:
    #                                                                                                 domain = get_domain(domain)
    #                                                                                             elif ".." in domain:
    #                                                                                                 domain = ""
    #                                                                                             else:
    #                                                                                                 domain = domain
    #                                                                                         else:
    #                                                                                             domain = ""
    #                                                                                     else:
    #                                                                                         domain = ""
    #                                                                                     phone_detail = re.findall(r'[\D]{0,7}[\D]{1}1[35789]\d{9,}', text)
    #                                                                                     phone_set = set()
    #                                                                                     phone = ""
    #                                                                                     if len(phone_detail) > 0:
    #                                                                                         phone_detail = phone_detail[0]
    #                                                                                         phone = re.findall(r'1[35789]\d{9,}', phone_detail)
    #                                                                                         if len(phone) > 0:
    #                                                                                             phone = phone[0]
    #                                                                                         else:
    #                                                                                             phone_detail = ""
    #                                                                                             phone = ""
    #                                                                                     else:
    #                                                                                         phone_detail = ""
    #                                                                                         phone = ""
    #                                                                                     qq_detail = re.findall(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', text)
    #                                                                                     if len(qq_detail)>0:
    #                                                                                         qq_detail = qq_detail[0]
    #                                                                                         qq = re.findall(r'[1-9][0-9]{4,14}', qq_detail)[0]
    #                                                                                     else:
    #                                                                                         qq_detail = ""
    #                                                                                         qq = ""
    #                                                                                     e_mail = re.findall(r'([a-zA-Z0-9_.+-]+@[a-fh-pr-zA-FH-PRZ0-9-]+\.[a-zA-Z0-9-.]+)', text)
    #                                                                                     if len(e_mail) > 0:
    #                                                                                         e_mail = e_mail[0]
    #                                                                                     else:
    #                                                                                         e_mail = ""
    #                                                                                     text = re.sub(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', ' ', text)
    #                                                                                     text = text.replace("，", " ").replace("。", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
    #                                                                                     weixinhaos_set = set()
    #                                                                                     weixinhao = ""
    #                                                                                     weixin = re.findall(r'[\s\S]{0,3}[\u4E00-\u9FA5 | \u0041-u005A | \u0061-\u007A]{1,4}[\s\S]{0,5}[A-Za-z0-9_-]{6,22}[^\s]+', text)
    #                                                                                     if len(weixin) > 0:
    #                                                                                         weixin = weixin[0]
    #                                                                                         weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
    #                                                                                         weixin_cut = weixin.replace(weixinhao, "") + weixinhao[0:2]
    #                                                                                         weixin_pinyin0 = lazy_pinyin(weixin_cut)
    #                                                                                         weixin_pinyins0 = ""
    #                                                                                         for j in weixin_pinyin0:
    #                                                                                             j = j.lower()
    #                                                                                             weixin_pinyins0 = weixin_pinyins0 + " " + j
    #                                                                                         weixin_pinyins0 = weixin_pinyins0.replace(
    #                                                                                             'nv', ' ').replace('lv',
    #                                                                                                                ' ').replace(
    #                                                                                             'wei bo', ' ')
    #                                                                                         if "❤" in weixin_pinyins0 or "v" in weixin_pinyins0 or "wei" in weixin_pinyins0 or "wx" in weixin_pinyins0 or "vx" in weixin_pinyins0 or "weix" in weixin_pinyins0 or "wei x" in weixin_pinyins0:
    #                                                                                             weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
    #                                                                                             if "vx" == weixinhao[:2].lower() or "wx" == weixinhao[:2].lower() and "wxid" != weixinhao[:4].lower():
    #                                                                                                 weixinhao = weixinhao[2:]
    #                                                                                             elif "v" == weixinhao[0].lower() and re.match(r'1[35789]\d{9,}', weixinhao[1:]):
    #                                                                                                 weixinhao = weixinhao[1:]
    #                                                                                             elif "wxid" == weixinhao[
    #                                                                                                            :4].lower():
    #                                                                                                 if "_" == weixinhao[5]:
    #                                                                                                     weixinhao = weixinhao
    #                                                                                                 else:
    #                                                                                                     weixinhao = weixinhao.replace(
    #                                                                                                         weixinhao[
    #                                                                                                             4], "_")
    #                                                                                             else:
    #                                                                                                 weixinhao = weixinhao
    #                                                                                         else:
    #                                                                                             if "@" in weixin or "#" in weixin:
    #                                                                                                 weixin = re.sub('[a-zA-Z]*v[a-zA-Z]*', ' ', weixin)
    #                                                                                             if weixin != []:
    #                                                                                                 weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)
    #                                                                                                 if len(weixinhao) > 0:
    #                                                                                                     weixinhao = weixinhao[0]
    #                                                                                                     i_1 = weixin.replace(weixinhao,"")
    #                                                                                                     i_1 = i_1.replace("加我","wei").replace("+","wei").replace("未","").replace("为","").replace("位","").replace("围","").replace("➕","wei").replace("喂","").replace("维","").replace("伟","").replace("唯","").replace("胃","").replace("卫","").replace("威","").replace("味","")
    #                                                                                                     weixin_pinyin = lazy_pinyin(i_1)
    #                                                                                                     weixin_pinyins = ""
    #                                                                                                     for j in weixin_pinyin:
    #                                                                                                         j = j.lower()
    #                                                                                                         weixin_pinyins = weixin_pinyins + ' '+ j
    #                                                                                                     i_2 = weixin_pinyins.replace("weibo", "").replace("nv", "").replace("lv", "").replace("wei bo", "")
    #                                                                                                     if "v" in i_2 or "wei" in i_2:
    #                                                                                                         weixin = weixin
    #                                                                                                         if "vx" == weixinhao[
    #                                                                                                                    -2:].lower():
    #                                                                                                             weixinhao = weixinhao[
    #                                                                                                                         :-2]
    #                                                                                                     else:
    #                                                                                                         weixin = ""
    #                                                                                                         weixinhao = ""
    #                                                                                                 else:
    #                                                                                                     weixin = ""
    #                                                                                                     weixinhao = ""
    #                                                                                             else:
    #                                                                                                 weixin = ""
    #                                                                                                 weixinhao = ""
    #                                                                                     else:
    #                                                                                         weixin = ""
    #                                                                                         weixinhao = ""
    #                                                                                     print(weixinhao, qq, phone, domain)
    #     #                                                                                 try:
    #     #                                                                                     # 先查有没有有效信息,再查有效信息在不在库里,不在则入库
    #     #                                                                                     if weixinhao or qq or phone or domain:
    #     #                                                                                         sql = 'SELECT DISTINCT weixinhao, qq, phone, domain FROM wa_key where source="%s"' % source
    #     #                                                                                         cursors.execute(sql)
    #     #                                                                                         db.commit()
    #     #                                                                                         results = set(cursors.fetchall())
    #     #                                                                                         if (weixinhao, qq, phone, domain) not in results:
    #     #                                                                                             sql = 'insert into wa_key(source, account_url, account_nickname, description, content, comments, crawl_time, publish_time, comments_nickname, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, domain, source_number) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d")' % (
    #     #                                                                                             source, account_url,
    #     #                                                                                             account_nickname, description,
    #     #                                                                                             content, comments, crawl_time,
    #     #                                                                                             publish_time, comments_nickname, isPass, weixin, weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone, e_mail, domain, 2)
    #     #                                                                                             cursors.execute(sql)
    #     #                                                                                             db.commit()
    #     #                                                                                 except Exception as e:
    #     #                                                                                     logger.error(e)
    #     #                                                                                     db.rollback()
    #     # db.close()
    # except Exception as e:
    #     logger.error(e)


if __name__ == '__main__':
    url_list = []
    url_sd_list = []
    url_tbxy_list = []
    url_yhk_list = []
    url_dbxyk_list = []
    url_fx_list = []
    url_fl_list = []
    url_sycz_list = []
    url_bc_list = []
    for i in range(1, 401):
        # url_tbxy = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%26t%3D0&page_type=searchall&page={}'.format(
        #     i)
        # url_tbxy_list.append(url_tbxy)
        # url_sd = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E5%88%B7%E5%8D%95%26t%3D0&page_type=searchall&page={}'.format(
        #     i)
        # url_sd_list.append(url_sd)
        # url_dbxyk = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E4%BB%A3%E5%8A%9E%E4%BF%A1%E7%94%A8%E5%8D%A1%26t%3D0&page_type=searchall&page={}'.format(
        #     i)
        # url_dbxyk_list.append(url_dbxyk)
        # url_yhk = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E9%93%B6%E8%A1%8C%E5%8D%A1%26t%3D0&page_type=searchall&page={}'.format(
        #     i)
        # url_yhk_list.append(url_yhk)
        # url_fx = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E8%BF%94%E7%8E%B0%26t%3D0&page_type=searchall&page={}'.format(
        #     i)
        # url_fx_list.append(url_fx)
        # url_fl = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E8%BF%94%E5%88%A9%26t%3D0&page_type=searchall&page={}'.format(
        #     i)
        # url_fl_list.append(url_fl)
        # url_sycz = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E6%89%8B%E6%B8%B8%E5%85%85%E5%80%BC%26t%3D0&page_type=searchall&page={}'.format(
        #     i)
        # url_sycz_list.append(url_sycz)
        url_bc = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D%E5%8D%9A%E5%BD%A9%26t%3D0&page_type=searchall&page={}'.format(i)
        url_bc_list.append(url_bc)
    url_list.extend(url_sd_list)
    url_list.extend(url_tbxy_list)
    url_list.extend(url_dbxyk_list)
    url_list.extend(url_yhk_list)
    url_list.extend(url_fl_list)
    url_list.extend(url_fx_list)
    url_list.extend(url_sycz_list)
    url_list.extend(url_bc_list)
    random.shuffle(url_list)
    pool = ThreadPool(8)
    pool.map(weibo_crawl, url_list)
    pool.close()
    pool.join()
