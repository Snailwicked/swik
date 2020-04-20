import json
import requests
import time
from lxml import etree
import os
from urllib.parse import parse_qs
import random
"""
爬取微博评论
"""

# proxies = ["222.85.28.130:52590","117.191.11.80:80","117.127.16.205:8080","118.24.128.46:1080","120.78.225.5:3128","113.124.92.200:9999","183.185.1.47:9797","115.29.3.37:80","36.248.129.158:9999","222.89.32.182:9999","117.191.11.111:80","182.35.84.182:9999","47.100.103.71:80","121.63.209.92:9999","124.193.37.5:8888","39.135.24.11:8080","14.146.95.4:9797","182.35.83.244:9999","113.120.36.179:9999","1.199.31.90:9999","58.17.125.215:53281","212.64.51.13:8888","182.35.84.135:9999","163.204.247.60:9999","39.106.35.21:3128","202.39.222.32:80","120.83.111.42:9999","63.220.1.43:80","42.238.85.70:9999","117.191.11.107:80"]

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'm.weibo.cn',
    'MWeibo-Pwa': '1',
    'Referer': 'https://m.weibo.cn/p/searchall?containerid=100103type%3D1%26q%3D%E6%B7%98%E5%AE%9D%E5%88%B7%E5%8D%95',
    'User-Agent': random.choice(USER_AGENTS),
    'X-Requested-With': 'XMLHttpRequest',
}

cookie = {'ALC': 'ac%3D2%26bt%3D1586505740%26cv%3D5.0%26et%3D1618041740%26ic%3D2044827766%26login_time%3D1586505738%26scf%3D%26uid%3D6506128896%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D76a7969a8c1decec2be0c9d7860c5857', 'LT': '1586505740', 'tgc': 'TGT-NjUwNjEyODg5Ng==-1586505739-gz-99B010C14A837B107CAF6DB9371CF881-1', 'ALF': '1618041740', 'SCF': 'AqJvyOQTdMOzpMQqbR6y9Zu-XBTp20YMeB6L4sOqi6JhKCFdt-7yetbVa2HDssz3zl_vsigImlTCd9lNzNhh5B8.', 'SUB': '_2A25zlFhcDeRhGeBL61QQ8ibEwjqIHXVQ4M6UrDV_PUNbm9AfLUjAkW9NR0wDx3ucdRGL2aRBfPlXPkM0YpVXdDV3', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5oh1C84Ps40UIv7gEFX-Aw5NHD95QcSK5ceKzR1h.cWs4DqcjTqJpf9PSk1KepSh2t', 'sso_info': 'v02m6alo5qztaKbh5WlnLW8uYyzhLSMkpm1mpaQvY2jlLCNo4SyjoOguY2gwMA='}


# 当前路径+pic
pic_file_path = os.path.join(os.path.abspath(''), 'pic')

# 下载图片
def download_pic(url, nick_name):
    if not url:
        return
    if not os.path.exists(pic_file_path):
        os.mkdir(pic_file_path)
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(pic_file_path + f'/{nick_name}.jpg', 'wb') as f:
            f.write(resp.content)

# 写入留言内容
def write_comment(comment):
    comment += '\n'
    with open('comment.txt', 'a', encoding='utf-8') as f:
        f.write(comment.replace('回复', '').replace('等人', '').replace('图片评论', ''))

# 获取子评论所需参数
comment_params = {
    'ajwvr': 6,
    'more_comment': 'big',
    'is_child_comment': 'true',
    'id': '4367970740108457',
    'from': 'singleWeiBo',
    'last_child_comment_id': '',
    'root_comment_id': '',
    'root_comment_max_id': ''
}

# 获取子评论，这里只是获取了第一页的子评论信息
def get_child_comment(root_comment_id):
    comment_params['root_comment_id'] = root_comment_id
    resp = requests.get(URL, params=comment_params, headers=headers,cookies=cookie)
    resp = json.loads(resp.text)
    if resp['code'] == '100000':
        html = resp['data']['html']
        from lxml import etree
        html = etree.HTML(html)
        # 每个子评论的节点
        data = html.xpath('//div[@class="WB_text"]')
        for i in data:
            nick_name = ''.join(i.xpath('./a/text()')).strip().replace('\n', '')
            comment = ''.join(i.xpath('./text()')).strip().replace('\n', '')
            write_comment(comment)
            # 获取图片对应的html节点
            pic = i.xpath('.//a[@action-type="widget_photoview"]/@action-data')
            pic = pic[0] if pic else ''
            if pic:
                # 拼接另外两个必要参数
                pic = pic + 'ajwvr=6&uid=5648894345'
                # 构造出一个完整的图片url
                url = 'https://weibo.com/aj/photo/popview?' + pic
                resp = requests.get(url, headers=headers,cookies=cookie)
                resp = resp.json()
                if resp.get('code') == '100000':
                    # 从突然url中，第一个就是评论中的图
                    url = resp['data']['pic_list'][0]['clear_picSrc']
                    # 下载图片
                    download_pic(pic_url, nick_name)
        print("子评论抓取完毕...")



if __name__ == '__main__':
    import requests

    cookies = {
        'SINAGLOBAL': '7911884340875.175.1533869578268',
        'UM_distinctid': '16fa7fbe38c1a8-0ffca21186b8af-366b400c-1fa400-16fa7fbe38d3e1',
        'SCF': 'Anc2d0DUHiUgtScfPqf0FqEgmsN1IwCUz2YktclWOhb9jEaVaxfZ_y5ollYhLzegwu76EXPw2wAQh8_5ShrCSk0.',
        'SUHB': '0G0-D4TFDxI26c',
        'ALF': '1616143412',
        'SUB': '_2AkMpKOq_dcPxrAVUmf4RyGvrbItH-jya_YNJAn7uJhIyOhhu7mkuqSVutBF-XHQBDAyPUbkBmj58AFzE4ZbvP1bD',
        'SUBP': '0033WrSXqPxfM72wWs9jqgMF55529P9D9WWzkvhSTbo-jcXKp8VaKYxp5JpX5KzhUgL.FoqfeKqXSh54ehq2dJLoI7vKdJ8Dd8YLxKqLBoML1K2t',
        'login_sid_t': '5a26b6f67424af6da61320ccb392e44f',
        'cross_origin_proto': 'SSL',
        'Ugrow-G0': '9ec894e3c5cc0435786b4ee8ec8a55cc',
        'YF-V5-G0': '99df5c1ecdf13307fb538c7e59e9bc9d',
        '_s_tentry': 'www.baidu.com',
        'UOR': ',,www.baidu.com',
        'wb_view_log': '1920*10801',
        'Apache': '8119825248635.131.1586506192963',
        'ULV': '1586506192968:76:1:1:8119825248635.131.1586506192963:1584686472436',
        'YF-Page-G0': '4358a4493c1ebf8ed493ef9c46f04cae|1586506195|1586506195',
    }

    headers = {
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://weibo.com/5044281310/ICyIMrBFW?type=comment',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    params = (
        ('ajwvr', '6'),
        ('id', '4491899366579684'),
        ('root_comment_max_id', '154098481851116'),
        ('root_comment_max_id_type', '0'),
        ('root_comment_ext_param', ''),
        ('page', '7'),
        ('filter', 'hot'),
        ('sum_comment_number', '11485'),
        ('filter_tips_before', '0'),
        ('from', 'singleWeiBo'),
        ('__rnd', '1586506869909'),
    )


    response = requests.get('https://weibo.com/aj/v6/comment/big', headers=headers, params=params, cookies=cookies)
    print(response.text)



    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4491899366579684&root_comment_max_id=152998972261120&root_comment_max_id_type=0&root_comment_ext_param=&page=7&filter=hot&sum_comment_number=11531&filter_tips_before=0&from=singleWeiBo&__rnd=1586506999540', headers=headers, cookies=cookies)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4491899366579684&root_comment_max_id=154098481851116&root_comment_max_id_type=0&root_comment_ext_param=&page=6&filter=hot&sum_comment_number=11485&filter_tips_before=0&from=singleWeiBo&__rnd=1586506869909', headers=headers, cookies=cookies)

    # params = {
    #     'ajwvr': 6,
    #     'id': '4491899366579684',
    #     'from': 'singleWeiBo',
    #     'root_comment_max_id': '166330550744093',
    #     'page': '5'
    #
    #
    # }
    # URL = 'https://weibo.com/aj/v6/comment/big'
    # # 爬去100页，需要代理，或者进行sleep 不然会超时。
    # for num in range(2):
    #     print(f'=========   正在读取第 {num} 页 ====================')
    #     # resp = requests.get(URL, params=params, headers=headers, proxies={"http": random.choices(proxies)[0]})
    #     resp = requests.get(URL, params=params, headers=headers,cookies=cookie)
    #     print(resp)
    #     resp = json.loads(resp.text)
    #     if resp['code'] == '100000':
    #         html = resp['data']['html']
    #
    #         html = etree.HTML(html)
    #         max_id_json = html.xpath('//div[@node-type="comment_loading"]/@action-data')[0]
    #
    #
    #         node_params = parse_qs(max_id_json)
    #         # max_id
    #         max_id = node_params['root_comment_max_id'][0]
    #         params['root_comment_max_id'] = max_id
    #         # data = html.xpath('//div[@class="list_ul"]/div[@node-type="root_comment"]/div[@class="list_con"]')
    #         data = html.xpath('//div[@node-type="root_comment"]')
    #         for i in data:
    #             # 评论人昵称
    #             nick_name = i.xpath('.//div[@class="WB_text"]/a/text()')[0]
    #             # 评论内容。
    #             # test = i.xpath('.//div[@class="WB_text"]/text()')
    #             wb_text = i.xpath('.//div[@class="WB_text"][1]/text()')
    #             string = ''.join(wb_text).strip().replace('\n', '')
    #             write_comment(string)
    #             # 评论id , 用于获取评论内容
    #             comment_id = i.xpath('./@comment_id')[0]
    #             # 评论的图片地址
    #             pic_url = i.xpath('.//li[@class="WB_pic S_bg2 bigcursor"]/img/@src')
    #             pic_url = 'https:' + pic_url[0] if pic_url else ''
    #             download_pic(pic_url, nick_name)
    #             # 查看评论
    #             get_child_comment(root_comment_id=comment_id)