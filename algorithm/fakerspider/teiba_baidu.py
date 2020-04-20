import requests
from lxml import etree
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import math
import json
import time
import datetime
import pymysql
from algorithm.fakerspider.tools import check_text, remove_emoji
from algorithm.fakerspider.tools import get_number,parse_content
from utils.headers import random_headers as headers

def get_links():
    '''
     'http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%CB%A2%B5%A5%20%2C%20%2BVX', # 刷单 , +VX
     'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E5%88%B7%E5%8D%95%2C%E5%BE%AE%E4%BF%A1&red_tag=w0862132222', # 刷单,微信
     'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E5%88%B7%E5%8D%95%2C%E5%A8%81%E4%BF%A1', # 刷单,威信
     'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%2C%2BVX&red_tag=e1106962408', # 淘宝信誉,+VX
     'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%2C%E5%BE%AE%E4%BF%A1', #淘宝信誉,微信
    :return:
    '''
    origin_urls = ['http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%CB%A2%B5%A5%20%2C%20%2BVX',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E5%88%B7%E5%8D%95%2C%E5%BE%AE%E4%BF%A1&red_tag=w0862132222',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E5%88%B7%E5%8D%95%2C%E5%A8%81%E4%BF%A1',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%2C%2BVX&red_tag=e1106962408',
                   'http://tieba.baidu.com/f/search/res?ie=utf-8&qw=%E6%B7%98%E5%AE%9D%E4%BF%A1%E8%AA%89%2C%E5%BE%AE%E4%BF%A1',
                  ]
    try:
        for origin_url in origin_urls:
            try:
                r = requests.get(url=origin_url, headers=headers, timeout=1.5).text
            except:
                continue
            html = etree.HTML(r)
            max_url_href = html.xpath('//div[@class="pager pager-search"]//a[@class="last"]/@href')
            max_page = max_url_href[0].split("pn=")[1]
            for i in range(1, int(max_page) + 1):
                url = origin_url + '&pn={}'.format(i)
                try:
                    r = requests.get(url=url, headers=headers,timeout=1.5).text
                except:
                    continue
                html = etree.HTML(r)
                tburlinfo_list = html.xpath('//div[@class="s_post_list"]/div//span[@class="p_title"]/a/@href')
                for tburlinfo in tburlinfo_list:
                    tburl = urljoin(url, tburlinfo)
                    yield tburl
    except requests.exceptions.RequestException as e:
        print(e)
#
db = pymysql.connect(host='180.97.15.181', port=3306, user='root', passwd='Vrv123!@#', db='fakespider', use_unicode=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursors = db.cursor()
#
#
def crawl():
    for url in get_links():
        print(url)
        try:
            r = requests.get(url=url, headers=headers, timeout=2).text
            html = etree.HTML(r)

            xpath_rule = ["//h3//text()", "//h1//text()"]
            account_nickname = remove_emoji(parse_content(html, xpath_rule))

            page = html.xpath('//span[@class="red"]/text()')[1]
            for i in range(1, int(page) + 1):
                temp_url = url.split('?')[0] + "?pn={}".format(i)
                try:
                    r = requests.get(url=temp_url, headers=headers, timeout=2).text
                except:
                    continue
                bs = BeautifulSoup(r, "html.parser")
                try:
                    html = bs.find(id="j_p_postlist").children
                except:
                    continue
                for ht in html:
                    html = etree.HTML(str(ht))
                    try:
                        temp_html = json.loads(html.xpath("//@data-field")[0])
                    except:
                        continue

                    try:
                        xpath_rule = ["//div[@class='d_post_content j_d_post_content clearfix']//text()",
                                      "//div[@class='d_post_content j_d_post_content']//text()"]
                        content = parse_content(html, xpath_rule)
                        if content == None or content == "":
                            content = ""
                    except Exception as e:
                        content = ""
                    try:
                        xpath_rule = ["//div[@class='post-tail-wrap']//span[4]//text()",
                                      "//ul[@class='p_tail']//li[2]//text()"]
                        time_list = parse_content(html, xpath_rule)
                        if time_list == None:
                            time_list = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        time_list = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

                    try:
                        xpath_rule = ["//div[@class='d_author']//ul//li[@class='d_name']//a//text()"]
                        comments_nickname = parse_content(html, xpath_rule)
                        if comments_nickname == None:
                            comments_nickname = ""
                    except:
                        comments_nickname = ""

                    comment_num = temp_html["content"]["comment_num"]
                    if comment_num:
                        page = math.ceil(comment_num / 10)
                        for i in range(1, page + 1):
                            try:
                                comment_num_url = "https://tieba.baidu.com/p/comment?tid={}&pid={}&pn={}&t={}".format(
                                temp_html["content"]["thread_id"], temp_html["content"]["post_id"], i,
                                int(round(time.time() * 1000)))
                            except:
                                continue
                            try:
                                r = requests.get(url=comment_num_url, headers=headers, timeout=2).text
                            except:
                                continue
                            bs = BeautifulSoup(r, "html.parser")
                            for item in bs.find_all(name="div", class_="lzl_cnt"):
                                item = etree.HTML(str(item))
                                comments_nickname = item.xpath("//a[1]//text()")[0]
                                comments = str(item.xpath("//span[@class='lzl_content_main']//text()")[0]).strip()
                                # coument_time = item.xpath("//span[@class='lzl_time']//text()")[0]

                                crawl_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                                isPass = 2
                                account_url = url
                                source = "百度贴吧-重点网站"
                                text = account_nickname.strip() + " " + content.strip() + " " + comments_nickname.strip()+" " + comments.strip()

                                if check_text(text):
                                    domain ,e_mail,website ,weixin ,weixinhao, qq,qq_detail, phone,phone_detail = get_number(text)
                                    data ={}
                                    data["weixinhao"] = weixinhao
                                    data["qq"] = qq
                                    data["phone"] = phone

                                    if weixinhao or qq or phone:
                                        print("联系方式", get_number(text))
                                        try:
                                            sql = 'SELECT DISTINCT weixinhao, qq, phone FROM wa_key where source="%s"' % source
                                            cursors.execute(sql)
                                            db.commit()
                                            results = cursors.fetchall()
                                            if {'weixinhao': weixinhao, 'qq': qq, 'phone': phone} not in results:
                                                sql = 'insert into wa_key(source, account_url, account_nickname, content, comments, crawl_time, publish_time, comments_nickname, post_id, isPass, weixin, weixinhao, qq_detail, qq, phone_detail, phone, e_mail, website) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
                                                    source, account_url, pymysql.escape_string(account_nickname),
                                                    pymysql.escape_string(content.strip()), pymysql.escape_string(comments), crawl_time, time_list,
                                                    pymysql.escape_string(comments_nickname), temp_html["content"]["post_id"], isPass, pymysql.escape_string(weixin),
                                                    weixinhao, pymysql.escape_string(qq_detail), qq, pymysql.escape_string(phone_detail), phone,
                                                    e_mail, website)
                                                print(sql)
                                                cursors.execute(sql)
                                                db.commit()
                                        except Exception as e:
                                            print(e)
                                            db.rollback()
        except:
            continue
try:
    crawl()
except Exception as e:
    print(e)
