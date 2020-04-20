import requests,json
from lxml import etree
from algorithm.fakerspider.tools import get_domain, is_borders
import datetime
from algorithm.fakerspider.store import DbToMysql

cookies = {
    'BIDUPSID': '2EBEF0AFA587D154535C8F1BB1875F2F',
    'PSTM': '1533712222',
    'BAIDUID': 'C16178459A21350BF66097CF13FB7E2A:FG=1',
    'BDUSS': 'oxMXljcUVDTGNpdzZleGljaVB-aG8wNGFqZllQaGlteX42SDNBdjV-cmFSMDVlSVFBQUFBJCQAAAAAAAAAAAEAAADfXm3MQmx1ZXNuYWlsMTk5OAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANq6Jl7auiZeaV',
    'BD_UPN': '12314753',
    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
    'MCITY': '-%3A',
    'BD_HOME': '1',
    'H_PS_PSSID': '30745_1442_21118_30792_30824_26350',
    'delPer': '0',
    'BD_CK_SAM': '1',
    'PSINO': '5',
    'COOKIE_SESSION': '87842_0_9_9_0_2_0_0_9_2_0_0_0_0_0_0_0_0_1582685729%7C9%233967869_64_1582529019%7C9',
    'H_PS_645EC': '7fccKMcnaxXhnL9U3a7A%2FuHXB5sQx4RU0TKz2EiXDKJayQhXqfp5b5eB51c',
}

configs = {'host': '180.97.15.181', 'user': 'root', 'password': 'Vrv123!@#', 'db': 'fakespider'}

requests.packages.urllib3.disable_warnings()
source = "搜索引擎-百度"
def crawl(url,params):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
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
    try:
        r = requests.get(url=url, headers=headers, params=params, cookies=cookies, timeout=3, verify=False).text
        html = etree.HTML(r)
    except Exception as e:
        print(e)
    datas = html.xpath('//div[@id="content_left"]')
    for item in datas:
        res_json = item.xpath('.//div[@class="c-tools"]/@data-tools')[0]
        res = json.loads(res_json)
        account_nickname = res["title"]
        url_temp = res['url']
        r = requests.get(url=url_temp, headers=headers, verify=False)
        account_url = r.url
        if "news" not in account_url and "bank" not in account_url:

            domain_temp = get_domain(account_url)
            if domain_temp and domain_temp not in white_set:
                '''
                检测境外网址无法访问
                '''
                # if is_borders(account_url):
                #     domain = domain_temp + "(境外)"
                # else:
                domain = domain_temp
                description = account_nickname
                crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                publish_time = datetime.datetime.today().strftime('%Y-%m-%d')
                data = {'source': source, 'account_url': account_url, 'account_nickname': account_nickname,
                        'crawl_time': crawl_time, 'description': description,
                        'publish_time': publish_time, 'domain': domain, 'isPass': '2', 'source_number': '2'}
                table = 'wa_key'
                print(data)
                dtm = DbToMysql(configs)
                all_domain = dtm.find_by_domain(source)
                unuserful_info = ['图片', '广告', '答案', '法律', '试题', '公积金', '检测中心', '快递', '房贷网', '信合',
                                  '消费', '维权', '培训', '新闻', '论坛', '软件', '购车', '计算器']
                unuserful_set = set(unuserful_info)
                if not any(i in account_nickname for i in unuserful_set):
                    if {'domain': domain} not in all_domain:
                        dtm.save_one_data(table, data)

if __name__ == '__main__':
    url = "https://www.baidu.com/s"
    for item in range(0,1000,10):
        for kw in ["\u4F4E\u989D\u8D37\u6B3E","\u94F6\u884C\u5361"]:
            params = (
                ('wd', '{}'.format(kw)),
                ('pn', '{}'.format(item)),
            )
            try:
                crawl(url,params)
            except:
                pass
    # baiduurl_list = ['https://www.baidu.com/s?wd={}&pn={}'.format(a, i)
    #                  for a in ['低额贷款', '银行卡'] for i in range(0, 200, 10)]
    # for item in baiduurl_list:
    #     print(item)
    #     crawl(item)

    # url = "https://www.baidu.com/s?wd=%E4%BD%8E%E9%A2%9D%E8%B4%B7%E6%AC%BE&pn=10"
