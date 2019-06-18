#!/usr/bin/env python
import requests
import time
import datetime
import re
import base64
import hmac
import hashlib
import matplotlib.pyplot as plt
from http import cookiejar
from PIL import Image
import threading
import json
from algorithm.fakerspider.tools import check_text, get_host
import pymysql
from pypinyin import lazy_pinyin


HEADERS = {
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
    }
LOGIN_URL = 'https://www.zhihu.com/signup'
LOGIN_API = 'https://www.zhihu.com/api/v3/oauth/sign_in'
FORM_DATA = {
    'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
    'grant_type': 'password',
    'source': 'com.zhihu.web',
    'username': '',
    'password': '',
    # 改为'cn'是倒立汉字验证码
    'lang': 'en',
    'ref_source': 'homepage'
}


class ZhihuAccount(object):

    def __init__(self):
        self.login_url = LOGIN_URL
        self.login_api = LOGIN_API
        self.login_data = FORM_DATA.copy()
        self.session = requests.session()
        self.session.headers = HEADERS.copy()
        self.session.cookies = cookiejar.LWPCookieJar(filename='./cookies.txt')

    def login(self, username=None, password=None, load_cookies=True):
        """
        模拟登录知乎
        :param username: 登录手机号
        :param password: 登录密码
        :param load_cookies: 是否读取上次保存的 Cookies
        :return: bool
        """
        if load_cookies and self.load_cookies():
            if self.check_login():
                return str(self.session.cookies)

        headers = self.session.headers.copy()
        headers.update({
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            #'X-Xsrftoken': self._get_token()  这个参数可以不要..... what's the fuck?
        })
        username, password = self._check_user_pass(username, password)
        self.login_data.update({
            'username': username,
            'password': password
        })
        timestamp = str(int(time.time()*1000))
        self.login_data.update({
            'captcha': self._get_captcha(self.login_data['lang'], headers),
            'timestamp': timestamp,
            'signature': self._get_signature(timestamp)
        })

        resp = self.session.post(self.login_api, data=self.login_data, headers=headers)
        if 'error' in resp.text:
            print(json.loads(resp.text)['error']['message'])
        elif self.check_login():
            return True
        print('登录失败')
        return False

    def load_cookies(self):
        """
        读取 Cookies 文件加载到 Session
        :return: bool
        """
        try:
            self.session.cookies.load(ignore_discard=True)
            return True
        except FileNotFoundError:
            return False

    def check_login(self):
        """
        检查登录状态，访问登录页面出现跳转则是已登录，
        如登录成功保存当前 Cookies
        :return: bool
        """
        resp = self.session.get(self.login_url, allow_redirects=False)
        if resp.status_code == 302:
            self.session.cookies.save()
            return True
        return False

    def _get_token(self):
        """
        从登录页面获取 token
        :return:
        """
        resp = self.session.get(self.login_url)
        token = resp.cookies['domain']
        return token


    def _get_captcha(self, lang, headers):
        """
        请求验证码的 API 接口，无论是否需要验证码都需要请求一次
        如果需要验证码会返回图片的 base64 编码
        根据 lang 参数匹配验证码，需要人工输入
        :param lang: 返回验证码的语言(en/cn)
        :param headers: 带授权信息的请求头部
        :return: 验证码的 POST 参数
        """
        if lang == 'cn':
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        else:
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        resp = self.session.get(api, headers=headers)
        show_captcha = re.search(r'true', resp.text)

        if show_captcha:
            put_resp = self.session.put(api, headers=headers)
            json_data = json.loads(put_resp.text)
            img_base64 = json_data['img_base64'].replace(r'\n', '')
            with open('./captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(img_base64))
            img = Image.open('./captcha.jpg')
            if lang == 'cn':
                plt.imshow(img)
                print('点击所有倒立的汉字，按回车提交')
                points = plt.ginput(7)
                capt = json.dumps({'img_size': [200, 44],
                                   'input_points': [[i[0]/2, i[1]/2] for i in points]})
            else:
                img.show()
                capt = input('请输入图片里的验证码：')
            # 这里必须先把参数 POST 验证码接口
            self.session.post(api, data={'input_text': capt}, headers=headers)
            return capt
        return ''

    def _get_signature(self, timestamp):
        """
        通过 Hmac 算法计算返回签名
        实际是几个固定字符串加时间戳
        :param timestamp: 时间戳
        :return: 签名
        """
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return ha.hexdigest()

    def _check_user_pass(self, username, password):
        """
        检查用户名和密码是否已输入，若无则手动输入
        """
        if username is None:
            username = self.login_data.get('username')
            if not username:
                username = input('请输入手机号：')
        if len(username) == 11 and username.isdigit() and '+86' not in username:
            username = '+86' + username

        if password is None:
            password = self.login_data.get('password')
            if not password:
                password = input('请输入密码：')
        return username, password

class ZhiHuCrawl:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = HEADERS.copy()

    def crawl(self, key_word, flag):
        db = pymysql.connect(host='', port=3306, user='root', passwd='', db='fakespider', use_unicode=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursors = db.cursor()
        headers = self.session.headers
        domain = headers['Host']
        headers.update({'cookie': flag})
        crawl_flag = 1
        i = -10
        while crawl_flag == 1:
            i += 10
            url = 'https://www.zhihu.com/api/v4/search_v3?t=people&q=%s&correction=1&offset=%d&limit=10&search_hash_id=047148667d9128530103f91eaa0e7b0b' % (key_word, int(i))
            resp = self.session.get(url=url, headers=headers)
            if resp.status_code == 200:
                res = json.loads(resp.text)
                if res['paging']['is_end'] == False:
                    infos = res['data']
                    for info in infos:
                        source = "知乎-重点网站"
                        isPass = 2
                        account_url_temp = info['object']['url']
                        account_url = account_url_temp.replace('api', 'www')
                        account_nickname = info['object']['name'].replace('<em>', '').replace('</em>', '')
                        content = info['highlight']['description'].replace('<em>', '').replace('</em>', '')
                        publish_time_temp = datetime.datetime.today()
                        publish_time = publish_time_temp.strftime('%Y-%m-%d')
                        crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        if account_nickname == None:
                            account_nickname = ""
                        if content == None:
                            content == ""
                        text = account_nickname.strip() + " " + content.strip()
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
                            weixin = re.findall(r'[\s\S]{0,3}[\u4E00-\u9FA5]{1,4}[\s\S]{0,5}[A-Za-z0-9_-]{6,22}[^\s]+', text)
                            if len(weixin)> 0:
                                weixin = weixin[0]
                                weixinhao = re.findall(r'[A-Za-z0-9_-]{6,22}', weixin)[0]
                                weixin_cut = weixin.replace(weixinhao, "") + weixinhao[0:2]
                                weixin_pinyin0 = lazy_pinyin(weixin_cut)
                                weixin_pinyins0 = ""
                                for j in weixin_pinyin0:
                                    j = j.lower()
                                    weixin_pinyins0 = weixin_pinyins0 + " " + j
                                if "❤" in weixin_pinyins0 or "v" in weixin_pinyins0 or "wx" in weixin_pinyins0 or "vx" in weixin_pinyins0 or "weix" in weixin_pinyins0 or "wei x" in weixin_pinyins0:
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
                                    sql = 'select DISTINCT weixinhao, qq, phone from wa_key where source="{}"'.format(source)
                                    cursors.execute(sql)
                                    db.commit()
                                    result = cursors.fetchall()
                                    if not {'weixinhao': weixinhao, 'qq': qq, 'phone': phone} in result:
                                        sql = 'insert into wa_key(source, account_url, account_nickname, content, publish_time, crawl_time, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, website) values("%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (source, account_url, pymysql.escape_string(account_nickname), pymysql.escape_string(content), publish_time, crawl_time, isPass, weixin, weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone, e_mail, website)
                                        cursors.execute(sql)
                                        db.commit()
                            except Exception as e:
                                print(e)
                                db.rollback()
                else:
                    crawl_flag = 0
        db.close()


if __name__ == '__main__':
    account = ZhihuAccount()
    flag = account.login()
    # flag为真就是登陆上去了,那么就去爬
    if flag:
        threads = []
        zhc = ZhiHuCrawl()
        key_words = ['淘宝刷单+VX', '淘宝信誉+VX', '银行卡+VX', '代办信用卡+VX', '返现+VX', '返利+VX']
        for key_word in key_words:
            thread = threading.Thread(target=zhc.crawl, args=(key_word, flag))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()







