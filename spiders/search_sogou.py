import requests, re,time
from lxml import etree
import datetime
from algorithm.fakerspider.store import DbToMysql
from utils.slave.extractors import ContentExtractor


from urllib.parse import urljoin
from requests import RequestException
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                         '/71.0.3578.10 Safari/537.36'}
# configs = {'host': '180.97.15.181', 'user': 'root', 'password': 'Vrv123!@#', 'db': 'fakespider'}
configs = {'host': '192.168.30.217', 'user': 'root', 'password': 'wzh234287', 'db': 'fakespider'}

requests.packages.urllib3.disable_warnings()
source = "搜索引擎-搜狗"
def crawl(url):

    try:
        r = requests.get(url=url, headers=headers, timeout=3, verify=False).text
        html = etree.HTML(r)
    except Exception as e:
        print(e)
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
                pass
            account_url = response.url
            print(account_url)
            ce = ContentExtractor(html=response.text, url=account_url)
            content = ce.get_content()
            date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", content)
            if date_all:
                publish_time = str(date_all[0])
            else:
                time_array = time.localtime(int(ce.get_publishing_date()/1000))
                publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
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
                        dtm.save_one_data(table, data)


if __name__ == '__main__':
    sougouurl_list = ['https://www.sogou.com/web?query=网警电话&pn={}'.format(i) for i in range(1, 101)]

    for item in sougouurl_list:
        # print(item)
        crawl(item)

    # url = "https://www.sogou.com/link?url=DSOYnZeCC_oFmTickJ_wj-BUVyL3lUU5TAuUMz5OmDyteaJZoPMQrCXw5Pqtik-2"
    # try:
    #     r = requests.get(url=url, headers=headers, timeout=3, verify=False).text
    #     p1 = r"https*://.*"
    #     pattern1 = re.compile(p1)
    #     jump_url = pattern1.findall(r)[0].split(')')[0]
    #     jump_url = jump_url.strip('"')
    #     response = requests.get(url=jump_url, headers=headers, timeout=3, verify=False)
    #     response.encoding = 'utf-8'
    # except RequestException as e:
    #     pass
    # print(response.url)
    # print(response.text)
    #
    # html = etree.HTML(response.content)
    # publish_time_list = html.xpath('//*[@class="user-txt"]/text()')
    # for publish_time in publish_time_list:
    #     publish_time = str(publish_time).strip("回答")
    # answers = html.xpath('//*[@class="replay-info-txt answer_con"]/text()')
    # print(answers)

    # for answer in answers:
    #     crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    #     content = ''.join(str(answer))

    # crawl(url)