# -*-coding:utf-8 -*-
import re
import os
import rsa
import math
import time
import random
import base64
import binascii
from urllib.parse import quote_plus
import requests
from algorithm.utils import code_verification
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

verify_code_path = './{}{}.png'
index_url = "http://weibo.com/login.php"


def get_pincode_url(pcid):
    size = 0
    url = "http://login.sina.com.cn/cgi/pin.php"
    pincode_url = '{}?r={}&s={}&p={}'.format(url, math.floor(random.random() * 100000000), size, pcid)
    return pincode_url


def get_img(url, name, retry_count):
    """
    :param url: url for verification code
    :param name: login account
    :param retry_count: retry number for getting verfication code
    :return:
    """
    pincode_name = verify_code_path.format(name, retry_count)
    resp = requests.get(url, headers=headers, stream=True)
    with open(pincode_name, 'wb') as f:
        for chunk in resp.iter_content(1000):
            f.write(chunk)
    return pincode_name


def get_encodename(name):
    # name must be string
    username_quote = quote_plus(str(name))
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


def get_server_data(su, session):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    prelogin_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(prelogin_url, headers=headers)

    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

    return sever_data


def get_password(password, servertime, nonce, pubkey):
    rsa_publickey = int(pubkey, 16)
    key = rsa.PublicKey(rsa_publickey, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    return passwd


# post data and get the next url
def get_redirect(name, data, post_url, session):
    logining_page = session.post(post_url, data=data, headers=headers)
    login_loop = logining_page.content.decode("GBK")

    # if name or password is wrong, set the value to 2
    if 'retcode=101' in login_loop:
        print('invalid password for {}, please ensure your account and password'.format(name))
        print('密码错误')
        # freeze_account(name, 2)
        return ''

    if 'retcode=2070' in login_loop:
        print('invalid verification code')
        return 'pinerror'

    if 'retcode=4049' in login_loop:
        print('account {} need verification for login'.format(name))
        return 'login_need_pincode'

    if '正在登录' or 'Signing in' in login_loop:
        pa = r'location\.replace\([\'"](.*?)[\'"]\)'
        return re.findall(pa, login_loop)[0]
    else:
        return ''


def login_no_pincode(name, password, session, server_data):
    post_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

    servertime = server_data["servertime"]
    nonce = server_data['nonce']
    rsakv = server_data["rsakv"]
    pubkey = server_data["pubkey"]
    sp = get_password(password, servertime, nonce, pubkey)

    data = {
        'encoding': 'UTF-8',
        'entry': 'weibo',
        'from': '',
        'gateway': '1',
        'nonce': nonce,
        'pagerefer': "",
        'prelt': 67,
        'pwencode': 'rsa2',
        "returntype": "META",
        'rsakv': rsakv,
        'savestate': '7',
        'servertime': servertime,
        'service': 'miniblog',
        'sp': sp,
        'sr': '1920*1080',
        'su': get_encodename(name),
        'useticket': '1',
        'vsnf': '1',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
    }

    rs = get_redirect(name, data, post_url, session)

    return rs, None, '', session


def login_by_pincode(name, password, session, server_data, retry_count):
    post_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

    servertime = server_data["servertime"]
    nonce = server_data['nonce']
    rsakv = server_data["rsakv"]
    pubkey = server_data["pubkey"]
    pcid = server_data['pcid']

    sp = get_password(password, servertime, nonce, pubkey)

    data = {
        'encoding': 'UTF-8',
        'entry': 'weibo',
        'from': '',
        'gateway': '1',
        'nonce': nonce,
        'pagerefer': "",
        'prelt': 67,
        'pwencode': 'rsa2',
        "returntype": "META",
        'rsakv': rsakv,
        'savestate': '7',
        'servertime': servertime,
        'service': 'miniblog',
        'sp': sp,
        'sr': '1920*1080',
        'su': get_encodename(name),
        'useticket': '1',
        'vsnf': '1',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'pcid': pcid
    }

    img_url = get_pincode_url(pcid)
    pincode_name = get_img(img_url, name, retry_count)
    verify_code, yundama_obj, cid = code_verification.code_verificate("wangminghui", "ydm012566",
                                                                      pincode_name)
    data['door'] = verify_code
    rs = get_redirect(name, data, post_url, session)

    os.remove(pincode_name)
    return rs, yundama_obj, cid, session


def login_retry(name, password, session, ydm_obj, cid, rs='pinerror', retry_count=0):
    while rs == 'pinerror':
        ydm_obj.report_error(cid)
        retry_count += 1
        session = requests.Session()
        su = get_encodename(name)
        server_data = get_server_data(su, session)
        rs, yundama_obj, cid, session = login_by_pincode(name, password, session, server_data, retry_count)
    return rs, ydm_obj, cid, session


def do_login(name, password):
    session = requests.Session()
    su = get_encodename(name)
    server_data = get_server_data(su, session)

    if server_data['showpin']:
        rs, yundama_obj, cid, session = login_by_pincode(name, password, session, server_data, 0)
        if rs == 'pinerror':
            rs, yundama_obj, cid, session = login_retry(name, password, session, yundama_obj, cid)

    else:
        rs, yundama_obj, cid, session = login_no_pincode(name, password, session, server_data)
        if rs == 'login_need_pincode':
            session = requests.Session()
            su = get_encodename(name)
            server_data = get_server_data(su, session)
            rs, yundama_obj, cid, session = login_by_pincode(name, password, session, server_data, 0)

            if rs == 'pinerror':
                rs, yundama_obj, cid, session = login_retry(name, password, session, yundama_obj, cid)
    return rs, yundama_obj, cid, session


def get_session(name, password):
    url, yundama_obj, cid, session = do_login(name, password)
    if url != '':
        return session

if __name__=='__main__':
    session = get_session('17512525156', 'weibo012566')
    print(session.cookies.get_dict())

