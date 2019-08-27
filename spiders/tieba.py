# -*- coding: utf-8 -*-

import requests
from lxml import etree
from urllib.parse import urljoin
import random
from multiprocessing.dummy import Pool as ThreadPool
import re,urllib
import json
import time
import datetime
import pymysql
from algorithm.fakerspider.tools import check_text, remove_emoji, get_host
from pypinyin import lazy_pinyin
import pysnooper
from urllib.parse import quote
import string

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Host': 'tieba.baidu.com',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
          }


@pysnooper.snoop()
def tieba_crawl(url):
    db = pymysql.connect(host='180.97.15.181', port=3306, user='root', passwd='Vrv123!@#', db='fakespider', use_unicode=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursors = db.cursor()
    #dtms = DbToMysql({"host":"180.97.15.181", "user":"root", "password":"Vrv123!@#", "db":"fakespider"})
    try:
        r = requests.get(url=url, headers=headers, timeout=2).text
        html = etree.HTML(r)
        if html.xpath('//h3[@class="core_title_txt pull-left text-overflow  "]/@title'):
            account_nickname = html.xpath('//h3[@class="core_title_txt pull-left text-overflow  "]/@title')[0]
            account_nickname = remove_emoji(account_nickname)
        elif html.xpath('//h1[@class="core_title_txt  "]/@title'):
            account_nickname = html.xpath('//h1[@class="core_title_txt  "]/@title')[0]
            account_nickname = remove_emoji(account_nickname)
        elif html.xpath('//h3[@class="core_title_txt pull-left text-overflow   vip_red "]/@title'):
            account_nickname = html.xpath('//h3[@class="core_title_txt pull-left text-overflow   vip_red "]/@title')[0]
            account_nickname = remove_emoji(account_nickname)
        if html.xpath('//span[@class="tP"]'):
            page = html.xpath('//span[@class="tP"]/text()')[0]
        else:
            page = 1
        info_list = html.xpath('//div[@class="p_postlist"]/div[@class="l_post l_post_bright j_l_post clearfix  "]')
        for info in info_list:
            data_temp = info.xpath('.//@data-field')[0] if info.xpath('.//@data-field') else None
            if data_temp:
                data = json.loads(data_temp)
                isPass = 2
                account_url = url
                source = "百度贴吧-重点网站"
                #楼层主贴,不包括评论回复
                content_temp = data["content"]["content"]
                if content_temp:
                    content = content_temp.replace('&quot', '').replace('br', '').replace('&nbsp', '').replace(';', '').replace('<>', '').replace(' ', '')
                    content = remove_emoji(content)
                    #pattern = re.compile(r'<[^>]+>')
                    #content = pattern.sub('', content_temp).replace('&quot', '').replace('br', '').replace('&nbsp; ', '')
                    crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    publish_time = info.xpath('.//div[@class="post-tail-wrap"]/span/text()')[-1].split()[0] if info.xpath('.//div[@class="post-tail-wrap"]/span/text()') else None
                    post_id = str(data["content"]["post_id"])
                    thread_id_temp = url.split('?')[0]
                    thread_id = thread_id_temp.split('/')[-1]
                    #判断楼层贴下面是否含有评论回复,有就抓
                    comments_num = data["content"]["comment_num"]
                    if comments_num == 0:
                        comments = ""
                        comments_nickname_temp = data["author"]["user_nickname"]
                        comments_nickname = comments_nickname_temp if comments_nickname_temp != None else data["author"]["user_name"]
                        comments_nickname = remove_emoji(comments_nickname)
                        # dtms.save_one_data('wa_key', {"source":source, "account_url":account_url, "content":content, "comments":comments, "crawl_time":crawl_time, "publish_time":publish_time, "comments_nickname":comments_nickname, "post_id":post_id})
                        # 没有评论
                        description = ""
                        if account_nickname == None:
                            account_nickname = ""
                        if content == None:
                            content = ""
                        if comments_nickname == None:
                            comments_nickname = ""
                        if comments == None:
                            comments = ""
                        text = account_nickname.strip() + " " + description.strip() + " " + content.strip() + " " + comments.strip()
                        if check_text(text):
                            website = re.search(r'(https?://)?([\da-z-]+)\.([\da-z\.-]*)[\.]*([a-z\.]{2,6})([/a-zA-Z0-9\.-]+)+/?', text)
                            if website:
                                website = website[0]
                                if ".." in website:
                                    website = ""
                            else:
                                website = ""
                            if website and website != "":
                                a = get_host(website)
                                if a and a != "":
                                    website = a
                                else:
                                    website = ""
                            phone_detail = re.findall(r'[\D]{0,7}[\D]{1}1[35789]\d{9,}', text)
                            if len(phone_detail) > 0:
                                phone_detail = phone_detail[0]
                                phone = re.findall(r'1[35789]\d{9,}', phone_detail)
                                if len(phone) > 0:
                                    phone = phone[0]
                                else:
                                    phone_detail = ""
                                    phone = ""
                            else:
                                phone_detail = ""
                                phone = ""
                            qq_detail = re.findall(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', text)
                            if len(qq_detail)>0:
                                qq_detail = qq_detail[0]
                                qq = re.findall(r'[1-9][0-9]{4,14}', qq_detail)[0]
                            else:
                                qq_detail = ""
                                qq = ""
                            e_mail = re.findall(r'([a-zA-Z0-9_.+-]+@[a-fh-pr-zA-FH-PRZ0-9-]+\.[a-zA-Z0-9-.]+)', text)
                            if len(e_mail) > 0:
                                e_mail = e_mail[0]
                            else:
                                e_mail = ""
                            text = re.sub(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', ' ', text)
                            text = text.replace("，", " ").replace("。", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
                            weixinhaos_set = set()
                            weixinhao = ""
                            weixin = re.findall(r'[\s\S]{0,3}[\u4E00-\u9FA5 | \u0041-u005A | \u0061-\u007A]{1,4}[\s\S]{0,5}[A-Za-z0-9_-]{6,22}[^\s]+', text)
                            if len(weixin) > 0:
                                weixin = weixin[0]
                                weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
                                weixin_cut = weixin.replace(weixinhao, "") + weixinhao[0:2]
                                weixin_pinyin0 = lazy_pinyin(weixin_cut)
                                weixin_pinyins0 = ""
                                for j in weixin_pinyin0:
                                    j = j.lower()
                                    weixin_pinyins0 = weixin_pinyins0 + " " + j
                                if any(e in weixin_pinyins0 for e in ["❤","v","wei","wx","vx","weix","wei x"]):
                                    if "：" in weixin:
                                        index = weixin.index('：')
                                        weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin[index:])[0]
                                    else:
                                        weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
                                    if "vx" == weixinhao[:2].lower() or "wx" == weixinhao[
                                                                                :2].lower() and "wxid" != weixinhao[
                                                                                                          :4].lower():
                                        weixinhao = weixinhao[2:]
                                    elif "v" == weixinhao[0].lower() and re.match(r'1[35789]\d{9,}', weixinhao[1:]):
                                        weixinhao = weixinhao[1:]
                                    elif "wxid" == weixinhao[:4].lower():
                                        if "_" == weixinhao[5]:
                                            weixinhao = weixinhao
                                        else:
                                            weixinhao = weixinhao.replace(weixinhao[4], "_")
                                    else:
                                        weixinhao = weixinhao
                                else:
                                    if "@" in weixin or "#" in weixin:
                                        weixin = re.sub('[a-zA-Z]*v[a-zA-Z]*', ' ', weixin)
                                    if weixin != []:
                                        weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)
                                        if len(weixinhao) > 0:
                                            weixinhao = weixinhao[0]
                                            i_1 = weixin.replace(weixinhao,"")
                                            i_1 = i_1.replace("加我","wei").replace("+","wei").replace("未","").replace("为","").replace("位","").replace("围","").replace("➕","wei").replace("喂","").replace("维","").replace("伟","").replace("唯","").replace("胃","").replace("卫","").replace("威","").replace("味","")
                                            weixin_pinyin = lazy_pinyin(i_1)
                                            weixin_pinyins = ""
                                            for j in weixin_pinyin:
                                                j = j.lower()
                                                weixin_pinyins = weixin_pinyins + ' '+ j
                                            i_2 = weixin_pinyins.replace("weibo", "").replace("nv", "").replace("lv", "").replace("wei bo", "")
                                            if "v" in i_2 or "wei" in i_2:
                                                weixin = weixin
                                                if "vx" == weixinhao[-2:].lower():
                                                    weixinhao = weixinhao[:-2]
                                            else:
                                                weixin = ""
                                                weixinhao = ""
                                        else:
                                            weixin = ""
                                            weixinhao = ""
                                    else:
                                        weixin = ""
                                        weixinhao = ""
                            else:
                                weixin = ""
                                weixinhao = ""
                            try:
                                if weixinhao or qq or phone:
                                    sql = 'SELECT DISTINCT weixinhao, qq, phone FROM wa_key where source="%s"' % source
                                    cursors.execute(sql)
                                    db.commit()
                                    results = cursors.fetchall()
                                    if {'weixinhao': weixinhao, 'qq': qq, 'phone': phone} not in results:
                                        sql = 'insert into wa_key(source, account_url, account_nickname, content, comments, crawl_time, publish_time, comments_nickname, post_id, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, website) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (source, account_url, pymysql.escape_string(account_nickname), pymysql.escape_string(content), pymysql.escape_string(comments), crawl_time, publish_time, pymysql.escape_string(comments_nickname), post_id, isPass, pymysql.escape_string(weixin), weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone, e_mail, website)
                                        cursors.execute(sql)
                                        db.commit()
                            except Exception as e:
                                print(e)
                                db.rollback()
                        '''
                        lock = threading.Lock()
                        lock.acquire()
                        sql = 'insert into wa_key(source, account_url, account_nickname, content, comments, crawl_time, publish_time, comments_nickname, post_id, ip) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (source, account_url, pymysql.escape_string(account_nickname), pymysql.escape_string(content), pymysql.escape_string(comments), crawl_time, publish_time, comments_nickname, post_id, ip)
                        cursors.execute(sql)
                        db.commit()
                        lock.release()
                        '''
                    else:
                        reply_api = "https://tieba.baidu.com/p/totalComment?tid=" + thread_id + "&pn={}".format(page)
                        resp = requests.get(url=reply_api, headers=headers, timeout=2.5)
                        if resp.status_code == 200:
                            res = json.loads(resp.text)
                            if res["errmsg"] == "success":
                                try:
                                    comments_list = res["data"]["comment_list"][post_id]["comment_info"]
                                    for i in comments_list:
                                        description = ""
                                        comments_temp = i["content"]
                                        if comments_temp:
                                            comments_temp = comments_temp.split(":", 1)[-1]
                                            comments = comments_temp.replace('&quot', '').replace('br', '').replace('&nbsp', '').replace(';', '').replace('<>', '').replace(' ','')
                                            comments = remove_emoji(comments)
                                            #pattern = re.compile(r'<[^>]+>')
                                            #comments = pattern.sub('', comments_temp).replace('&quot', '').replace('br', '')
                                            comments_nickname = i["username"]
                                            comments_nickname = remove_emoji(comments_nickname)
                                            #dtms.save_one_data('wa_key', {"source":source, "account_url":account_url, "content":content, "comments":comments, "crawl_time":crawl_time, "publish_time":publish_time, "comments_nickname":comments_nickname, "post_id":post_id})
                                            # 有评论
                                            if account_nickname == None:
                                                account_nickname = ""
                                            if description == None:
                                                description = ""
                                            if content == None:
                                                content = ""
                                            if comments == None:
                                                comments = ""
                                            if comments_nickname == None:
                                                comments_nickname = ""
                                            text = account_nickname.strip() + " " + description.strip() + " " + content.strip() + " " + comments.strip()
                                            if check_text(text):
                                                website = re.search(r'(https?://)?([\da-z-]+)\.([\da-z\.-]*)[\.]*([a-z\.]{2,6})([/a-zA-Z0-9\.-]+)+/?', text)
                                                if website:
                                                    website = website[0]
                                                    if ".." in website:
                                                        website = ""
                                                else:
                                                    website = ""
                                                if website and website != "":
                                                    a = get_host(website)
                                                    if a and a != "":
                                                        website = a
                                                    else:
                                                        website = ""
                                                phone_detail = re.findall(r'[\D]{0,7}[\D]{1}1[35789]\d{9,}', text)
                                                phone_set = set()
                                                phone = ""
                                                if len(phone_detail) > 0:
                                                    phone_detail = phone_detail[0]
                                                    phone = re.findall(r'1[35789]\d{9,}', phone_detail)
                                                    if len(phone) > 0:
                                                        phone = phone[0]
                                                    else:
                                                        phone_detail = ""
                                                        phone = ""
                                                else:
                                                    phone_detail = ""
                                                    phone = ""
                                                qq_detail = re.findall(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', text)
                                                if len(qq_detail)>0:
                                                    qq_detail = qq_detail[0]
                                                    qq = re.findall(r'[1-9][0-9]{4,14}', qq_detail)[0]
                                                else:
                                                    qq_detail = ""
                                                    qq = ""
                                                e_mail = re.findall(r'([a-zA-Z0-9_.+-]+@[a-fh-pr-zA-FH-PRZ0-9-]+\.[a-zA-Z0-9-.]+)', text)
                                                if len(e_mail) > 0:
                                                    e_mail = e_mail[0]
                                                else:
                                                    e_mail = ""
                                                text = re.sub(r'[Qq扣秋]{1,2}[Qq:：扣号秋 是]{0,4}[1-9][0-9]{4,14}', ' ', text)
                                                text = text.replace("，", " ").replace("。", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
                                                weixinhaos_set = set()
                                                weixinhao = ""
                                                weixin = re.findall(r'[\s\S]{0,3}[\u4E00-\u9FA5 | \u0041-u005A | \u0061-\u007A]{1,4}[\s\S]{0,5}[A-Za-z0-9_-]{6,22}[^\s]+', text)
                                                if len(weixin)> 0:
                                                    weixin = weixin[0]
                                                    weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
                                                    weixin_cut = weixin.replace(weixinhao, "") + weixinhao[0:2]
                                                    weixin_pinyin0 = lazy_pinyin(weixin_cut)
                                                    weixin_pinyins0 = ""
                                                    for j in weixin_pinyin0:
                                                        j = j.lower()
                                                        weixin_pinyins0 = weixin_pinyins0 + " " + j
                                                    if "❤" in weixin_pinyins0 or "v" in weixin_pinyins0 or "wei" in weixin_pinyins0 or "wx" in weixin_pinyins0 or "vx" in weixin_pinyins0 or "weix" in weixin_pinyins0 or "wei x" in weixin_pinyins0:
                                                        if "：" in weixin:
                                                            index = weixin.index('：')
                                                            weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin[index:])[0]
                                                        else:
                                                            weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
                                                        if "vx" == weixinhao[:2].lower() or "wx" == weixinhao[:2].lower() and "wxid" != weixinhao[:4].lower():
                                                            weixinhao = weixinhao[2:]
                                                        elif "v" == weixinhao[0].lower() and re.match(r'1[35789]\d{9,}',
                                                                                                      weixinhao[1:]):
                                                            weixinhao = weixinhao[1:]
                                                        elif "wxid" == weixinhao[:4].lower():
                                                            if "_" == weixinhao[5]:
                                                                weixinhao = weixinhao
                                                            else:
                                                                weixinhao = weixinhao.replace(weixinhao[4], "_")
                                                        else:
                                                            weixinhao = weixinhao
                                                    else:
                                                        if "@" in weixin or "#" in weixin:
                                                            weixin = re.sub('[a-zA-Z]*v[a-zA-Z]*', ' ', weixin)
                                                        if weixin != []:
                                                            weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)
                                                            if len(weixinhao) > 0:
                                                                weixinhao = weixinhao[0]
                                                                i_1 = weixin.replace(weixinhao,"")
                                                                i_1 = i_1.replace("加我","wei").replace("+","wei").replace("未","").replace("为","").replace("位","").replace("围","").replace("➕","wei").replace("喂","").replace("维","").replace("伟","").replace("唯","").replace("胃","").replace("卫","").replace("威","").replace("味","")
                                                                weixin_pinyin = lazy_pinyin(i_1)
                                                                weixin_pinyins = ""
                                                                for j in weixin_pinyin:
                                                                    j = j.lower()
                                                                    weixin_pinyins = weixin_pinyins + ' '+ j
                                                                i_2 = weixin_pinyins.replace("weibo", "").replace("nv", "").replace("lv", "").replace("wei bo", "")
                                                                if "v" in i_2 or "wei" in i_2:
                                                                    weixin = weixin
                                                                    if "vx" == weixinhao[-2:].lower():
                                                                        weixinhao = weixinhao[:-2]
                                                                else:
                                                                    weixin = ""
                                                                    weixinhao = ""
                                                            else:
                                                                weixin = ""
                                                                weixinhao = ""
                                                        else:
                                                            weixin = ""
                                                            weixinhao = ""
                                                else:
                                                    weixin = ""
                                                    weixinhao = ""
                                                try:
                                                    if weixinhao or qq or phone:
                                                        sql = 'SELECT DISTINCT weixinhao, qq, phone FROM wa_key where source="%s"' % source
                                                        cursors.execute(sql)
                                                        db.commit()
                                                        results = cursors.fetchall()
                                                        if {'weixinhao': weixinhao, 'qq': qq, 'phone': phone} not in results:
                                                            sql = 'insert into wa_key(source, account_url, account_nickname, content, comments, crawl_time, publish_time, comments_nickname, post_id, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, website) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (source, account_url, pymysql.escape_string(account_nickname),pymysql.escape_string(content), pymysql.escape_string(comments), crawl_time, publish_time, pymysql.escape_string(comments_nickname), post_id, isPass, pymysql.escape_string(weixin), weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone, e_mail, website)
                                                            cursors.execute(sql)
                                                            db.commit()
                                                except Exception as e:
                                                    print(e)
                                                    db.rollback()
                                            '''
                                            lock = threading.Lock()
                                            lock.acquire()
                                            sql = 'insert into wa_key(source, account_url, account_nickname, content, comments, crawl_time, publish_time, comments_nickname, post_id, ip) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (source, account_url, pymysql.escape_string(account_nickname),pymysql.escape_string(content), pymysql.escape_string(comments), crawl_time, publish_time, comments_nickname, post_id, ip)
                                            cursors.execute(sql)
                                            db.commit()
                                            lock.release()
                                            '''
                                except Exception as e:
                                    print(e)
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == '__main__':


    # key_words = ["刷单,+VX","刷单,微信","刷单,威信","淘宝信誉,+VX","淘宝信誉,微信","淘宝信誉,威信","代办信用卡,微信"]

    origin_urls = ['http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%CB%A2%B5%A5%20%2C%20%2BVX',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E5%88%B7%E5%8D%95%2C%E5%BE%AE%E4%BF%A1',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E5%88%B7%E5%8D%95%2C%E5%A8%81%E4%BF%A1',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%2C%2BVX',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%2C%E5%BE%AE%E4%BF%A1',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%2C%E5%A8%81%E4%BF%A1',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E4%BB%A3%E5%8A%9E%E4%BF%A1%E7%94%A8%E5%8D%A1%2C%E5%BE%AE%E4%BF%A1',
                  ]
    tburl_list = []


    try:
        for origin_url in origin_urls:
            r = requests.get(url=origin_url, headers=headers, timeout=1.5).text
            html = etree.HTML(r)
            max_url_href = html.xpath('//div[@class="pager pager-search"]/a[@class="last"]/@href')[0] if html.xpath('//div[@class="pager pager-search"]/a[@class="last"]/@href') else None
            if max_url_href:
                max_page = max_url_href.split("pn")[1].replace("=", '')
                for i in range(1, int(max_page)+1):
                    url = origin_url + '&pn={}'.format(i)
                    r = requests.get(url=url, headers=headers).text
                    html = etree.HTML(r)
                    tburlinfo_list = html.xpath('//div[@class="s_post_list"]/div')
                    for tburlinfo in tburlinfo_list:
                        tburl_temp = tburlinfo.xpath('.//span[@class="p_title"]/a/@href')[0] if tburlinfo.xpath('.//span[@class="p_title"]/a/@href') else None
                        tburl = urljoin(url, tburl_temp)
                        tburl_list.append(tburl)
    except requests.exceptions.RequestException as e:
        print(e)
    pool = ThreadPool(8)
    pool.map(tieba_crawl, tburl_list)
    pool.close()
    pool.join()
