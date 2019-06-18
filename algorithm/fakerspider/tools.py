from lxml import etree
import re
from urllib.parse import urlparse
import json
import time
import socket
import random
import requests


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
    domain_temp = urlparse(website)[1]
    index = domain_temp.index('.')
    domain = domain_temp[index+1:]
    return domain