from utils.headers import random_headers as headers
import time,re
from dateutil.parser import parse as date_parser
import requests
from utils.tools import removehtml
import json

class WeiBo_Spider:

    def __int__(self):
        self.page = 20

    def get_comments(self,params):
        # account_id = item["mblog"]["user"]["id"]  # 账号id
        # news_id = item["mblog"]["mid"]  # 账号id
        # params = (
        #     ('id', '{}'.format(account_id)),
        #     ('mid', '{}'.format(news_id)),
        #     ('max_id_type', '0'),
        # )
        response = requests.get('https://m.weibo.cn/comments/hotflow', headers=headers, params=params)
        results = json.loads(response.text)
        if results["ok"] == 1:
            print("---------------评论数据----------------")
            for item in results["data"]["data"]:
                comment_publish_time = int(time.mktime(date_parser(str(item["created_at"])).timetuple()) * 1000)
                print("评论发布时间：",comment_publish_time,"*********","评论发布作者：",item["user"]["screen_name"])
                print("评论内容：",removehtml(item["text"]))
            if results["data"]["max_id"]:
                print("获取第二页评论数据需登录")
                # new_parms = list(params)
                # new_parms.append(("max_id", "{}".format(results["data"]["max_id"])))
                # get_comments(tuple(new_parms))
        else:
            print("---------------没有评论数据------------")

    def get_info(self):
        for page in range(2, 21):
            params = (
                ('containerid', '100103type=1&q=%E4%B8%AD%E5%85%B4'),
                ('page_type', 'searchall'),
                ('page', '{}'.format(page)),
            )
            response = requests.get('https://m.weibo.cn/api/container/getIndex', headers=headers, params=params)
            results = json.loads(response.text)
            if results["ok"] == 1:
                info_list_temp = results["data"]["cards"]

                for item in info_list_temp:
                    content_info = {}
                    content_info["source"] = "新浪微博"
                    content_info["url"] = item["scheme"]

                    publish_time = item["itemid"].split("&")[-2].split("=")[-1]
                    content_info["publish_time"] = publish_time
                    content_info["content"] = removehtml(item["mblog"]["text"])

                    account_nickname = item["mblog"]["user"]["screen_name"]  # 个人账号昵称
                    content_info["author"] = account_nickname

                    print(content_info)
if __name__ == '__main__':
    weibo_spider= WeiBo_Spider()
    weibo_spider.get_info()




