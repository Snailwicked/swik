import requests
from lxml import etree
import threading
import logging
from urllib.parse import urljoin
from requests import RequestException
import re
import datetime
from algorithm.fakerspider.store import DbToMysql
from algorithm.fakerspider.tools import get_domain, is_borders
import json
import time
import urllib3


urllib3.disable_warnings()
logging.basicConfig(level=logging.WARNING, filename='search_enginelog.txt', filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
configs = {'host': '180.97.15.181', 'user': 'root', 'password': 'Vrv123!@#', 'db': 'fakespider'}


def search_crawl(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                             '/71.0.3578.10 Safari/537.36'}
    try:
        r = requests.get(url=url, headers=headers, timeout=3, verify=False).text
    except RequestException as e:
        logger.warning(e)
    else:
        source = "搜索引擎"
        html = etree.HTML(r)
        if 'sogou' in url:
            results = html.xpath('//div[@class="results"]/div[@class="vrwrap"]')
            for result in results:
                href = result.xpath('.//h3[@class="vrTitle"]/a[@target="_blank"]/@href')[0] if \
                    result.xpath('.//h3[@class="vrTitle"]/a[@target="_blank"]/@href') else ''
                if href:
                    detail_url = urljoin(url, href)
                    # 标题
                    fake_account_nickname = result.xpath('(.//h3[@class="vrTitle"]/a/em/text() |'
                                                         ' .//h3[@class="vrTitle"]/a/text())')
                    account_nickname = ''.join(str(d) for d in fake_account_nickname)
                    join_dict = {account_nickname: detail_url}
                    if "百度知道" in account_nickname:
                        try:
                            # url通过js方法转换了
                            r = requests.get(url=join_dict[account_nickname], headers=headers, timeout=3, verify=False).text
                            p1 = r"https*://.*"
                            pattern1 = re.compile(p1)
                            jump_url = pattern1.findall(r)[0].split(')')[0]
                            jump_url = jump_url.strip('"')
                            response = requests.get(url=jump_url, headers=headers, timeout=3, verify=False)
                            response.encoding = 'utf-8'
                        except RequestException as e:
                            logger.warning(e)
                        else:
                            # 百度知道的网页结构
                            html = etree.HTML(response.content)
                            publish_time_list = html.xpath('//*[@class="wgt-replyer-all-time"]/text()')
                            for publish_time in publish_time_list:
                                publish_time = str(publish_time)
                            answers = html.xpath('//*[@accuse="aContent"]/text()')
                            for answer in answers:
                                crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                                content = ''.join(str(answer))
                                account_url = jump_url
                                if "电话" in content:
                                    phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d+",
                                                              content)
                                    if len(phone_detail) > 0:
                                        if phone_detail[0] == "110":
                                            pass
                                        else:
                                            phone = phone_detail[0]
                                            if len(phone) >= 5:
                                                dtm = DbToMysql(configs)
                                                all_url = dtm.find_by_account_url(source)
                                                if {'account_url': account_url} not in all_url:
                                                    table = 'wa_key'
                                                    data = {'source': source, 'account_url': account_url,
                                                            'account_nickname': account_nickname, 'content': content,
                                                            'crawl_time': crawl_time, 'publish_time': publish_time,
                                                            'phone': phone, 'isPass': '2', 'source_number': '2'}
                                                    dtm.save_one_data(table, data)

                                else:
                                    phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d{7,8}",
                                                              content)
                                    if len(phone_detail) > 0:
                                        phone = phone_detail[0]
                                        dtm = DbToMysql(configs)
                                        all_url = dtm.find_by_account_url(source)
                                        if {'account_url': account_url} not in all_url:
                                            table = 'wa_key'
                                            data = {'source': source, 'account_url': account_url,
                                                    'account_nickname': account_nickname, 'content': content,
                                                    'crawl_time': crawl_time, 'publish_time': publish_time,
                                                    'phone': phone, 'isPass': '2', 'source_number': '2'}
                                            dtm.save_one_data(table, data)

                    elif "搜狗问问" in account_nickname:
                        try:
                            r = requests.get(url=join_dict[account_nickname], headers=headers, timeout=3, verify=False).text
                            p1 = r"https*://.*"
                            pattern1 = re.compile(p1)
                            jump_url = pattern1.findall(r)[0].split(')')[0]
                            jump_url = jump_url.strip('"')
                            response = requests.get(url=jump_url, headers=headers, timeout=3, verify=False)
                            response.encoding = 'utf-8'
                        except RequestException as e:
                            logger.warning(e)
                        else:
                            # 搜狗问问的网页结构
                            html = etree.HTML(response.content)
                            publish_time_list = html.xpath('//*[@class="user-txt"]/text()')
                            for publish_time in publish_time_list:
                                publish_time = str(publish_time).strip("回答")
                            answers = html.xpath('//*[@class="replay-info-txt answer_con"]/text()')
                            for answer in answers:
                                crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                                content = ''.join(str(answer))
                                account_url = jump_url
                                if "电话" in content:
                                    phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d+",
                                                              content)
                                    if len(phone_detail) > 0:
                                        if phone_detail[0] == "110":
                                            pass
                                        else:
                                            phone = phone_detail[0]
                                            if len(phone) >= 5:
                                                dtm = DbToMysql(configs)
                                                all_url = dtm.find_by_account_url(source)
                                                if {'account_url': account_url} not in all_url:
                                                    table = 'wa_key'
                                                    data = {'source': source, 'account_url': account_url,
                                                            'account_nickname': account_nickname, 'content': content,
                                                            'crawl_time': crawl_time, 'publish_time': publish_time,
                                                            'phone': phone, 'isPass': '2', 'source_number': '2'}
                                                    dtm.save_one_data(table, data)

                                else:
                                    phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d{7,8}",
                                                              content)
                                    if len(phone_detail) > 0:
                                        phone = phone_detail[0]
                                        dtm = DbToMysql(configs)
                                        all_url = dtm.find_by_account_url(source)
                                        if {'account_url': account_url} not in all_url:
                                            table = 'wa_key'
                                            data = {'source': source, 'account_url': account_url,
                                                    'account_nickname': account_nickname, 'content': content,
                                                    'crawl_time': crawl_time, 'publish_time': publish_time,
                                                    'phone': phone, 'isPass': '2', 'source_number': '2'}
                                            dtm.save_one_data(table, data)
        elif "贷款" or "银行卡" in url:
            white_list = ['icbc.com.cn', 'ccb.com', 'abchina.com', 'boc.cn', 'bankcomm.com', 'psbc.com', 'cmbchina.com',
                          'cib.com.cn', 'citicbank.com', 'pingan.com', 'cebbank.com', 'cdb.com.cn', 'hxb.com.cn',
                          'eximbank.gov.cn', 'cmbc.com.cn', 'rong360.com', 'baidu.com', '10086.cn', 'qq.com',
                          'sohu.com',
                          'focus.cn', '58.com', 'so.com', 'sogou.com', 'bilibili.com', 'ganji.com', 'fang.com', 'cn',
                          'csls.cdb.com.cn', '95599.cn', 'ihouze.com', 'baixing.com', 'ooopic.com', 'china-cmca.org',
                          'com', 'cbrc.gov.cn', 'cardcn.com', 'bosc.cn', 'gdnybank.com', 'ksrcb.cn', 'yin68.com',
                          'qdccb.com', 'tzbank.com', 'creditcard.com.cn', 'boimc.com.cn', 'ctrip.com',
                          'wjrcb.com', 'bankofliaoyang.net', 'lccb.com.cn', 'taccb.com.cn', 'wzcb.com.cn',
                          'suzhoubank.com', 'qrcb.com.cn', 'bgzchina.com', 'bankofdl.com', 'bangrong.com', 'snccb.com',
                          'tccb.com.cn', 'cpic.com.cn', 'aliyun.com', 'xcnzxx.com', 'shudouzi.com', '163.com',
                          'alipay.cn', 'alipay.com', 'alipaydev.com', 'fund123.cn', 'mybank.cn', 'xin.xin', 'zhima.xin',
                          'zhimaxy.com.cn', 'zhisheng.com', 'zmxy.com.cn', 'jx-bank.com', 'huawei.com', 'xncredit.com']
            white_set = set(white_list)
            datas = html.xpath('//div[@class="f13"]')
            for data in datas:
                res_json = data.xpath('.//div[@class="c-tools"]/@data-tools')[0]
                res = json.loads(res_json)
                account_nickname = res["title"]
                url_temp = res['url']
                r = requests.get(url=url_temp, headers=headers, verify=False)
                account_url = r.url
                if "news" not in account_url and "bank" not in account_url:
                    domain_temp = get_domain(account_url)
                    if domain_temp and domain_temp not in white_set:
                        if is_borders(account_url):
                            domain = domain_temp + "(境外)"
                        else:
                            domain = domain_temp
                        description = account_nickname
                        crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        publish_time = datetime.datetime.today().strftime('%Y-%m-%d')
                        data = {'source': source, 'account_url': account_url, 'account_nickname': account_nickname,
                                'crawl_time': crawl_time, 'description': description,
                                'publish_time': publish_time, 'domain': domain, 'isPass': '2', 'source_number': '2'}
                        table = 'wa_key'
                        dtm = DbToMysql(configs)
                        all_domain = dtm.find_by_domain(source)
                        unuserful_info = ['图片', '广告', '答案', '法律', '试题', '公积金', '检测中心', '快递', '房贷网', '信合',
                                          '消费', '维权', '培训', '新闻', '论坛', '软件', '购车', '计算器']
                        unuserful_set = set(unuserful_info)
                        if not any(i in account_nickname for i in unuserful_set):
                            if {'domain': domain} not in all_domain:
                                dtm.save_one_data(table, data)

        else:
            # 360进来的网警电话
            results = html.xpath('//ul[@class="result"]/li[@class="res-list"]')
            for result in results:
                fake_account_nickname = result.xpath('.//div[@class="mh-title-wrap"]/a/text() | '
                                                     './/div[@class="mh-title-wrap"]/a/em/text() | '
                                                     './/h3[@class="res-title "]/a/text() | .'
                                                     '//h3[@class="res-title "]/a/em/text() | '
                                                     './/h3[@class="title"]/a/text() | '
                                                     './/h3[@class="title"]/a/em/text() | '
                                                     './/h3[@class="res-title"]/a/text() | '
                                                     './/h3[@class="res-title"]/a/em/text()')
                href = result.xpath('.//div[@id="mohe-biu_wenda_stract"]'
                                    '/div[@class="mohe-wrap"]/div[@class="mh-card-wrap"]'
                                    '/div[@class="mh-title-wrap"]/a/@href |'
                                    ' .//h3[@class="res-title "]/a/@href |'
                                    ' .//h3[@class="title"]/a/@href |'
                                    ' .//h3[@class="res-title"]/a/@href')[0]
                if href:
                    # 百度知道的url是直接给的不需要转
                    if "zhidao.baidu.com" in href:
                        try:
                            r = requests.get(url=href, headers=headers, timeout=3, verify=False)
                            r.encoding = 'utf-8'
                        except Exception as e:
                            logger.warning(e)
                        else:
                            account_nickname = ''.join(str(i) for i in fake_account_nickname)
                            html = etree.HTML(r.content)
                            publish_time_list = html.xpath('//*[@class="wgt-replyer-all-time"]/text()')
                            for publish_time in publish_time_list:
                                publish_time = str(publish_time)
                            answers = html.xpath('//*[@accuse="aContent"]/text()')
                            for answer in answers:
                                crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                                content = ''.join(answer)
                                account_url = href
                                if "电话" in content:
                                    phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d+",
                                                              content)
                                    if len(phone_detail) > 0:
                                        if phone_detail[0] == "110":
                                            pass
                                        else:
                                            phone = phone_detail[0]
                                            if len(phone) >= 5:
                                                dtm = DbToMysql(configs)
                                                all_url = dtm.find_by_account_url(source)
                                                if {'account_url': account_url} not in all_url:
                                                    table = 'wa_key'
                                                    data = {'source': source, 'account_url': account_url,
                                                            'account_nickname': account_nickname, 'content': content,
                                                            'crawl_time': crawl_time, 'publish_time': publish_time,
                                                            'phone': phone, 'isPass': '2', 'source_number': '2'}
                                                    dtm.save_one_data(table, data)

                                else:
                                    phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d{7,8}",
                                                              content)
                                    if len(phone_detail) > 0:
                                        phone = phone_detail[0]
                                        dtm = DbToMysql(configs)
                                        all_url = dtm.find_by_account_url(source)
                                        if {'account_url': account_url} not in all_url:
                                            table = 'wa_key'
                                            data = {'source': source, 'account_url': account_url,
                                                    'account_nickname': account_nickname, 'content': content,
                                                    'crawl_time': crawl_time, 'publish_time': publish_time,
                                                    'phone': phone, 'isPass': '2', 'source_number': '2'}
                                            dtm.save_one_data(table, data)

                    else:
                        # 360问答和搜狗问问要转化下url
                        r = requests.get(url=href, verify=False, headers=headers).text
                        p1 = r"https*://.*"
                        pattern1 = re.compile(p1)
                        jump_url_temp = pattern1.findall(r)[0].split(')')[0] if pattern1.findall(r) else ''
                        if jump_url_temp:
                            jump_url = jump_url_temp.replace('http', 'https')
                            jump_url = jump_url.strip('"')
                            account_nickname = ''.join(str(d) for d in fake_account_nickname)
                            if "wenda.so.com" in jump_url:
                                try:
                                    response = requests.get(url=jump_url, headers=headers, timeout=3, verify=False).text
                                except RequestException as e:
                                    logger.warning(e)
                                else:
                                    html = etree.HTML(response)
                                    publish_time = html.xpath('//div[@class="text"]/span[3]/text()')[0]
                                    publish_time = publish_time.replace('.', '-')
                                    crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                                    answer = html.xpath('//div[@class="bd"]/div[@class="resolved-cnt"]/text() | '
                                                        '//div[@class="bd"]/div[@class="resolved-cnt src-import"]'
                                                        '/p/text()')
                                    content = ''.join(str(a) for a in answer)
                                    account_url = jump_url
                                    if "电话" in content:
                                        phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d+",
                                                                  content)
                                        if len(phone_detail) > 0:
                                            if phone_detail[0] == "110":
                                                pass
                                            else:
                                                phone = phone_detail[0]
                                                if len(phone) >= 5:
                                                    dtm = DbToMysql(configs)
                                                    all_url = dtm.find_by_account_url(source)
                                                    if {'account_url': account_url} not in all_url:
                                                        table = 'wa_key'
                                                        data = {'source': source, 'account_url': account_url,
                                                                'account_nickname': account_nickname, 'content': content,
                                                                'crawl_time': crawl_time, 'publish_time': publish_time,
                                                                'phone': phone, 'isPass': '2', 'source_number': '2'}
                                                        dtm.save_one_data(table, data)

                                    else:
                                        phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d{7,8}",
                                                                  content)
                                        if len(phone_detail) > 0:
                                            phone = phone_detail[0]
                                            dtm = DbToMysql(configs)
                                            all_url = dtm.find_by_account_url(source)
                                            if {'account_url': account_url} not in all_url:
                                                table = 'wa_key'
                                                data = {'source': source, 'account_url': account_url,
                                                        'account_nickname': account_nickname, 'content': content,
                                                        'crawl_time': crawl_time, 'publish_time': publish_time,
                                                        'phone': phone, 'isPass': '2', 'source_number': '2'}
                                                dtm.save_one_data(table, data)

                            elif "wenwen.sogou.com" in jump_url:
                                try:
                                    response = requests.get(url=jump_url, headers=headers, timeout=3, verify=False).text
                                except RequestException as e:
                                    logger.warning(e)
                                else:
                                    html = etree.HTML(response)
                                    publish_time_list = html.xpath('//*[@class="user-txt"]/text()')
                                    for publish_time in publish_time_list:
                                        publish_time = str(publish_time).strip("回答")
                                    answers = html.xpath('//div[@id="bestAnswers"]//'
                                                         'pre[@class="replay-info-txt answer_con"]//text()')
                                    content = ''.join(answers)
                                    crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                                    account_url = jump_url
                                    if "电话" in content:
                                        phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d+",
                                                                  content)
                                        if len(phone_detail) > 0:
                                            if phone_detail[0] == "110":
                                                pass
                                            else:
                                                phone = phone_detail[0]
                                                if len(phone) >= 5:
                                                    dtm = DbToMysql(configs)
                                                    all_url = dtm.find_by_account_url(source)
                                                    if {'account_url': account_url} not in all_url:
                                                        table = 'wa_key'
                                                        data = {'source': source, 'account_url': account_url,
                                                                'account_nickname': account_nickname, 'content': content,
                                                                'crawl_time': crawl_time, 'publish_time': publish_time,
                                                                'phone': phone, 'isPass': '2', 'source_number': '2'}
                                                        dtm.save_one_data(table, data)

                                    else:
                                        phone_detail = re.findall(r"\d{3}-\d{7,8}|\d{4}-\d{7,8}|1[35789]\d{9,}|\d{7,8}",
                                                                  content)
                                        if len(phone_detail) > 0:
                                            phone = phone_detail[0]
                                            dtm = DbToMysql(configs)
                                            all_url = dtm.find_by_account_url(source)
                                            if {'account_url': account_url} not in all_url:
                                                table = 'wa_key'
                                                data = {'source': source, 'account_url': account_url,
                                                        'account_nickname': account_nickname, 'content': content,
                                                        'crawl_time': crawl_time, 'publish_time': publish_time,
                                                        'phone': phone, 'isPass': '2', 'source_number': '2'}
                                                dtm.save_one_data(table, data)


if __name__ == '__main__':

    url_list = []
    threads = []
    qihuurl_list1 = ['https://www.so.com/s?q=网警电话&pn={}'.format(i) for i in range(1, 21)]
    qihuurl_list2 = ['https://www.so.com/s?q=网警电话是多少&pn={}'.format(i) for i in range(1, 21)]
    sougouurl_list = ['https://www.sogou.com/web?query=网警电话&pn={}'.format(i) for i in range(1, 21)]
    url_list.extend(qihuurl_list1)
    url_list.extend(qihuurl_list2)
    url_list.extend(sougouurl_list)
    baiduurl_list = ['https://www.baidu.com/s?wd={}&pn={}'.format(a, i)
                     for a in ['低额贷款', '银行卡'] for i in range(0, 200, 10)]
    url_list.extend(baiduurl_list)
    for url in url_list:
        thread = threading.Thread(target=search_crawl, args=(url,))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()

