import sys
import uuid
import hashlib
from importlib import reload
import requests
import time
import json
reload(sys)
YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '2f630863bdd83784'
APP_SECRET = 'joRKV8XZoPwOOeXZbsRvyegJR5JTZqVP'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def connect(q):
    data = {}
    data['from'] = 'en'
    data['to'] = 'zh'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        return response.text

def translation(content):
    content_len = len(content)
    if content_len > 4000:
        paragraph_list = content.split("\n")
        new_list = []
        temp_string = ""
        p_words_num_sum = 0
        article_zh = ""
        for p in paragraph_list:
            p_words_num = len(p)
            p_words_num_sum = p_words_num + p_words_num_sum
            if p_words_num_sum < 4000:
                temp_string = temp_string + p + "\n"
            else:
                new_list.append(temp_string)
                temp_string = p + "\n"
                p_words_num_sum = p_words_num
        for itme in new_list:
            result = connect(itme)
            result = json.loads(result)
            article_zh = article_zh + result.get("translation")[0] + "\n"
    else:
        result = connect(content)
        result = json.loads(result)
        article_zh = result.get("translation")[0]
    return article_zh

#
# text = "Rapid DNA Machines in Police Departments Need Regulation"
# print(translation(text))