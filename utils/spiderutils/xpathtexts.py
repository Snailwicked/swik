# -*- coding: utf-8 -*-
import requests,re
from lxml import etree
'''
传入url,header通过xPath路径获取html中的数据
用法：
    url = "http://www.sohu.com/a/304311876_123753"
    X_path= "//article[@class = 'article']//p//text()"
    header = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',}
    xpt = xPathTexts()
    contens = xpt.get_contents(url,X_path,header)
'''
class xPathTexts(object):
    def __init__(self, url = None,X_path=None ,header = None):
        self.url = url
        self.X_path = X_path
        self.contents = []
        self.headers = header

    def getHtml(self):
        '''
        获取self.url 的 html
        :return: html
        '''
        resp = requests.get(self.url,headers= self.headers)
        charset = None
        try:
            reg = '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?'
            bianma = re.findall(reg, resp.text)[0][1]
        except:
            bianma = ""
        if bianma!="":
            charset = bianma.lower()
        resp.encoding = charset
        return resp.text

    def get_contents(self,*args,**kwargs):
        '''
        :param url: 'http://www.sohu.com/a/304311876_123753'
        :param X_path: '//article[@class = 'article']//p//text()'
        :param header: {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',}
        :return: '原标题：日媒：日本新年号拟于4月1日中午前后公布中新网3月28日电 据日本共同社报道，当地时间27日，多名相关人士透露，日本政府已为4月1日中午'
        '''
        self.url = url
        self.X_path = X_path
        self.contents = []
        self.headers = header
        self.html = self.getHtml()
        contens = []
        for item in etree.HTML(str(self.html)).xpath(self.X_path):
            contens.append(str(item).strip())
        return contens
if __name__ == "__main__":
    url = "http://www.sohu.com/a/304311876_123753"
    X_path= "//article[@class = 'article']//p//text()"
    header = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',}
    xpt = xPathTexts()
    contens = xpt.get_contents(url=url,X_path=X_path,header=header)
    for item in contens:
        print(item)