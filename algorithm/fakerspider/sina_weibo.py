from utils.headers import random_headers as headers
import time,re
from dateutil.parser import parse as date_parser
from algorithm.fakerspider.tools import check_text, remove_emoji, get_domain,get_number

import pymysql

def removehtml(html):
    p = re.compile('<[^>]+>')
    return p.sub("", html)


def check(text):
    pass
    # if weixinhao or qq or phone or domain:
    #     sql = 'SELECT DISTINCT weixinhao, qq, phone, domain FROM wa_key where source="%s"' % source
    #     cursors.execute(sql)
    #     db.commit()
    #     results = set(cursors.fetchall())
    #     if (weixinhao, qq, phone, domain) not in results:
    #         sql = 'insert into wa_key(source, account_url, account_nickname, description, content, comments, crawl_time, publish_time, comments_nickname, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, domain, source_number) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d")' % (
    #             source, account_url,
    #             pymysql.escape_string(account_nickname), pymysql.escape_string(description),
    #             pymysql.escape_string(content), pymysql.escape_string(comments), crawl_time,
    #             publish_time, comments_nickname, isPass, weixin, weixinhao, pymysql.escape_string(qq_detail), qq,
    #             pymysql.escape_string(phone_detail), phone, e_mail, domain, 2)


def get_comments(params,content_info):
    response = requests.get('https://m.weibo.cn/comments/hotflow', headers=headers, params=params,timeout=2)
    content_info["account_url"] = response.url
    result = []
    content_info["crawl_time"] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    results = json.loads(response.text)
    if results["ok"] == 1:
        for item in results["data"]["data"]:
            comment_publish_time = int(time.mktime(date_parser(str(item["created_at"])).timetuple()) * 1000)
            # print("评论发布时间：",comment_publish_time,"*********","评论发布作者：",item["user"]["screen_name"])
            new_content_info = content_info.copy()
            new_content_info["comments_nickname"] = item["user"]["screen_name"]
            new_content_info["comments"] = removehtml(item["text"])
            result.append(new_content_info)
            # print("评论内容：",removehtml(item["text"]))
        if results["data"]["max_id"]:
            print("获取第二页评论数据需登录")
            # new_parms = list(params)
            # new_parms.append(("max_id", "{}".format(results["data"]["max_id"])))
            # get_comments(tuple(new_parms)
        return result
    else:
        content_info["comments_nickname"] = ""
        content_info["comments"] = ""
        result.append(content_info)
        return result




# db = pymysql.connect(host='180.97.15.181', port=3306, user='root', passwd='Vrv123!@#', db='fakespider', use_unicode=True, charset='utf8mb4')
db = pymysql.connect(host='192.168.30.217', port=3306, user='root', passwd='wzh234287', db='fakespider', use_unicode=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

cursors = db.cursor()


def start(params):
    response = requests.get('https://m.weibo.cn/api/container/getIndex', headers=headers, params=params,timeout=2)
    print(response.url)
    results = json.loads(response.text)
    if results["ok"] == 1:
        info_list_temp = results["data"]["cards"]

        for item in info_list_temp:
            isPass = 2
            source = "新浪微博-重点网站"
            content_info = {}
            content_info["source"] = source
            content_info["isPass"] = isPass

            publish_time = item["itemid"].split("&")[-2].split("=")[-1]
            # print("发布时间：",publish_time)
            # print("文本内容：",)
            content_info["publish_time"] = time.strftime('%Y-%m-%d', time.localtime(int(publish_time)))

            content_info["content"] = removehtml(item["mblog"]["text"])

            account_id = item["mblog"]["user"]["id"]  # 账号id
            news_id = item["mblog"]["mid"]  # 账号id
            # print("账号id：",account_id)
            account_nickname = item["mblog"]["user"]["screen_name"]  # 个人账号昵称
            content_info["account_nickname"] = account_nickname
            account_url = item["mblog"]["user"]["profile_url"]  # 个人账号主页地址
            # print("主页地址：",account_url)

            description = item["mblog"]["user"]["description"].strip()  # 个人简介
            content_info["description"] = description

            params = (
                ('id', '{}'.format(account_id)),
                ('mid', '{}'.format(news_id)),
                ('max_id_type', '0'),
            )
            try:
                result = get_comments(params, content_info)
                for item in result:
                    print(item)
                    text = item["description"].strip() + " " + item["content"].strip() + " " + item[
                        "comments"].strip() + " "
                    if check_text(text):
                        domain, e_mail, website, weixin, weixinhao, qq, qq_detail, phone, phone_detail = get_number(
                            text)
                        if weixinhao or qq or phone or domain:
                            sql = 'SELECT DISTINCT weixinhao, qq, phone, domain FROM wa_key where source="%s"' % source
                            cursors.execute(sql)
                            db.commit()
                            results = set(cursors.fetchall())
                            if (weixinhao, qq, phone, domain) not in results:
                                sql = 'insert into wa_key(source, account_url, account_nickname, description, content, comments, crawl_time, publish_time, comments_nickname, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, domain, source_number) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d")' % (
                                    source, account_url,
                                    account_nickname, description,
                                    content_info["content"], item["comments"], item["crawl_time"],
                                    content_info["publish_time"], item["comments_nickname"], isPass, weixin, weixinhao,
                                    pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone,
                                    e_mail, domain, 2)
                                print(content_info)
                                cursors.execute(sql)
                                db.commit()
            except Exception as e:
                print(e)
            finally:
                text = item["description"].strip() + " " + item["content"].strip()
                if check_text(text):
                    domain, e_mail, website, weixin, weixinhao, qq, qq_detail, phone, phone_detail = get_number(
                        text)
                    if weixinhao or qq or phone or domain:
                        sql = 'SELECT DISTINCT weixinhao, qq, phone, domain FROM wa_key where source="%s"' % source
                        cursors.execute(sql)
                        db.commit()
                        results = set(cursors.fetchall())
                        if (weixinhao, qq, phone, domain) not in results:
                            sql = 'insert into wa_key(source, account_url, account_nickname, description, content, comments, crawl_time, publish_time, comments_nickname, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, domain, source_number) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d")' % (
                                source, account_url,
                                account_nickname, description,
                                content_info["content"], item["comments"], item["crawl_time"],
                                content_info["publish_time"], item["comments_nickname"], isPass, weixin, weixinhao,
                                pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone,
                                e_mail, domain, 2)
                            print(content_info)
                            cursors.execute(sql)
                            db.commit()
import json
if __name__ == '__main__':
    import requests
    keword =["手游充值","博彩","返利","返现","银行卡","代办信用卡","刷单","淘宝信誉"]
    for page in range(2,40):
        for ke in keword:
            params = (
                ('containerid', '100103type=1&q={}'.format(ke)),
                ('page_type', 'searchall'),
                ('page', '{}'.format(page)),
            )
            # start(params)
            try:
                start(params)
            except Exception as e:
                print(e)





