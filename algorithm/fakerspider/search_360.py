import requests,json,re
from lxml import etree
from algorithm.fakerspider.tools import get_domain, is_borders
import datetime
from algorithm.fakerspider.store import DbToMysql
from algorithm.fakerspider.tools import get_number,parse_content
cookies = {
    '$Cookie: __huid': '11HGgxWodKG97zfn33N%2Bz7vpWw4ewskSjoUiznVzYM%2FjM%3D',
    '__DC_gid': '9114931.187358221.1546519824080.1553582054483.9',
    'QiHooGUID': '3CFDDBB0F4AEC07EE1AA74D6CF0BE108.1579225605836',
    '__guid': '15484592.2851820944917829600.1579225606565.9148',
    'dpr': '1',
    'webp': '1',
    'stc_ls_sohome': 'RQz02jYRKf\\u0021tTRXfM(WM',
    '__gid': '9114931.187358221.1546519824080.1579229789800.54',
    'screenw': '1',
    'opqopq': 'b605b975f82f6d85a0ba30fe737e6f84.1582695792',
    'gtHuid': '1',
    '_S': 'n8b66q96u026b43qi1l4h6lgm4',
    'count': '6',
}

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
configs = {'host': '180.97.15.181', 'user': 'root', 'password': 'Vrv123!@#', 'db': 'fakespider'}

requests.packages.urllib3.disable_warnings()
source = "搜索引擎"
def crawl(url):
    try:
        r = requests.get(url=url, headers=headers, timeout=3, verify=False).text
    except Exception as e:
       return
    html = etree.HTML(r)
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
        print(fake_account_nickname)
        href = result.xpath('.//div[@id="mohe-biu_wenda_stract"]'
                            '/div[@class="mohe-wrap"]/div[@class="mh-card-wrap"]'
                            '//div[@class="mh-title-wrap"]/a/@href |'
                            ' .//h3[@class="res-title "]/a/@href |'
                            ' .//h3[@class="title"]/a/@href |'
                            ' .//h3[@class="res-title"]/a/@href')
        if href:
            # href = href[0]
            # 百度知道的url是直接给的不需要转
            if "zhidao.baidu.com" in href:
                try:
                    r = requests.get(url=href, headers=headers, timeout=3, verify=False)
                    r.encoding = 'utf-8'
                except Exception as e:
                    print(e)
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
                                            print(data)
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
                                    print(data)
                                    dtm.save_one_data(table, data)

            else:
                # 360问答和搜狗问问要转化下url
                try:
                    r = requests.get(url=href, verify=False, headers=headers).text
                except:
                    continue
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
                        except Exception as e:
                            print(e)
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
                                                print(data)
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
                                        print(data)
                                        dtm.save_one_data(table, data)

                    elif "wenwen.sogou.com" in jump_url:
                        try:
                            response = requests.get(url=jump_url, headers=headers, timeout=3, verify=False).text
                        except Exception as e:
                            print(e)
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
                                                print(data)
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
                                        print(data)
                                        dtm.save_one_data(table, data)


if __name__ == '__main__':

    for page in range(1,21):
        for kw in ["\u7F51\u8B66\u7535\u8BDD\u662F\u591A\u5C11","\u7F51\u8B66\u7535\u8BDD"]:


            params = (
                ('q', '{}'.format(kw)),
                ('pn', '{}'.format(page)),
            )
            print(params)
    # url_list = []
    # qihuurl_list1 = ['https://www.so.com/s?q=网警电话&pn={}'.format(i) for i in range(1, 21)]
    # qihuurl_list2 = ['https://www.so.com/s?q=网警电话是多少&pn={}'.format(i) for i in range(1, 21)]
    # url_list.extend(qihuurl_list1)
    # url_list.extend(qihuurl_list2)
    #
    # for item in url_list:
    #     print(item)
    #     get_number

    # url = "https://www.baidu.com/s?wd=低额贷款&pn=10"
    # crawl(url)