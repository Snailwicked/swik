from lxml import etree
import re
from urllib.parse import urlparse
import json
import time
import socket
import random
import requests
from pypinyin import lazy_pinyin


def parse_content(html,xpath_rule):
    for xpath in xpath_rule:
        account_nickname_list = html.xpath(xpath)
        if len(account_nickname_list):
            return account_nickname_list[0]


# 去除emoji表情符号
def remove_emoji(text):
    try:
        text = str(text,"utf-8")
    except TypeError as e:
        pass
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return highpoints.sub(u'', text)


# 从获取的文本中(包含几个字段)检查是否含反诈骗要的关键词(提高准备率)
def check_text(text):
    keywords = ["刷单", "淘宝信誉", "低额贷款", "代办信用卡", "返现", "返利", "充值"]
    if any([i in text for i in keywords]):
        return True
    return False


# 把网址转化为域名然后再判断是境内还是境外
def get_host(website):
    res = urlparse(website)[1]
    if res:
        try:
            myaddr = socket.getaddrinfo(res, 'http')
            ip = myaddr[0][4][0]
        except Exception as e:
            print(e)
        else:
            if ip:
                try:
                    time.sleep(random.random()*5)
                    r = requests.get(url='http://www.ip138.com/ips1388.asp?ip=%s&action=2' % ip, timeout=4)
                except Exception as e:
                    print(e)
                else:
                    if r.status_code == 200:
                        r.encoding = 'gb2312'
                        html = etree.HTML(r.text)
                        location = html.xpath('//table[@width="80%"]/tr[3]/td/ul/li[1]/text()')[0]
                        data = location.split('：')[1]
                        str_list = ["省", "市"]
                        if any(word in data for word in str_list):
                            pass
                        else:
                            return website


def is_borders(website):
    """
    返回境外域名
    :param website:str
    :return: domain:str
    """
    domain = urlparse(website)[1]
    if domain:
        try:
            myaddr = socket.getaddrinfo(domain, 'http')
            ip = myaddr[0][4][0]
            print(ip)
        except Exception as e:
            print(e)
        else:
            if ip:
                i = 0
                while i < 3:
                    try:
                        time.sleep(random.random()*5)
                        r = requests.get(url='http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
                    except Exception as e:
                        print(e)
                        i += 1
                    else:
                        if r.status_code == 200:
                            data = json.loads(r.text)
                            if data['code'] == 0:
                                country = data['data']['country']
                                if country == "中国":
                                    pass
                                else:
                                    index = domain.index('.')
                                    domain = domain[index + 1:]
                                    return domain
                            else:
                                i += 1


def get_domain(website):
    """
    返回域名
    :param website: str
    :return: domain :str
    """
    try:
        domain_temp = urlparse(website)[1]
        index = domain_temp.index('.')
        domain = domain_temp[index+1:]
    except:
        return ""
    return domain

def insert_data(db,data,source,sql):
    cursors = db.cursor()
    try:
        sql_select = 'SELECT DISTINCT weixinhao, qq, phone FROM wa_key where source="%s"' % source
        cursors.execute(sql_select)
        db.commit()
        results = cursors.fetchall()
        if {'weixinhao': data["weixinhao"], 'qq':data["qq"] , 'phone': data["phone"]} not in results:
            cursors.execute(sql)
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()

def get_number(text):
    domain = re.search(r'(https?://)?([\da-z-]+)\.([\da-z\.-]*)[\.]*([a-z\.]{2,6})([/a-zA-Z0-9\.-]+)+/?', text)
    if domain:
        domain = domain[0]
        if "www" in domain:
            domain = get_domain(domain)
        elif ".." in domain:
            domain = ""
        else:
            domain = domain
    else:
        domain = ""

    website = re.search(r'(https?://)?([\da-z-]+)\.([\da-z\.-]*)[\.]*([a-z\.]{2,6})([/a-zA-Z0-9\.-]+)+/?',text)
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
    if len(qq_detail) > 0:
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
    text = text.replace("，", " ").replace("。", " ").replace("  ", " ").replace("  ", " ").replace("  ",
                                                                                                  " ").replace(
        "  ", " ")
    weixin = re.findall(
        r'[\s\S]{0,3}[\u4E00-\u9FA5 | \u0041-u005A | \u0061-\u007A]{1,4}[\s\S]{0,5}[A-Za-z0-9_-]{6,22}[^\s]+',
        text)
    if len(weixin) > 0:
        weixin = weixin[0]
        weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
        weixin_cut = weixin.replace(weixinhao, "") + weixinhao[0:2]
        weixin_pinyin0 = lazy_pinyin(weixin_cut)
        weixin_pinyins0 = ""
        for j in weixin_pinyin0:
            j = j.lower()
            weixin_pinyins0 = weixin_pinyins0 + " " + j
        if any(e in weixin_pinyins0 for e in ["❤", "v", "wei", "wx", "vx", "weix", "wei x"]):
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
                    i_1 = weixin.replace(weixinhao, "")
                    i_1 = i_1.replace("加我", "wei").replace("+", "wei").replace("未", "").replace("为",
                                                                                                "").replace(
                        "位", "").replace("围", "").replace("➕", "wei").replace("喂", "").replace("维",
                                                                                               "").replace(
                        "伟", "").replace("唯", "").replace("胃", "").replace("卫", "").replace("威",
                                                                                            "").replace("味",
                                                                                                        "")
                    weixin_pinyin = lazy_pinyin(i_1)
                    weixin_pinyins = ""
                    for j in weixin_pinyin:
                        j = j.lower()
                        weixin_pinyins = weixin_pinyins + ' ' + j
                    i_2 = weixin_pinyins.replace("weibo", "").replace("nv", "").replace("lv", "").replace(
                        "wei bo", "")
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
    return domain ,e_mail,website ,weixin ,weixinhao, qq, qq_detail,phone,phone_detail

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Host': 'tieba.baidu.com',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
          }