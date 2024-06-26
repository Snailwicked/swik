# -*- coding: utf-8 -*-
import requests,re
from lxml import etree
from utils.headers import random_headers

class xPathTexts(object):

    def __int__(self):
        pass


    def getHtml(self):
        '''
        获取self.url 的 html
        :return: html
        '''
        if self.headers== None:
            self.headers = random_headers
        try:
            resp = requests.get(url=self.url, headers=self.headers, cookies=self.cookies , timeout=3)
            if resp.status_code ==200:
                reg = '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?'
                try:
                    charset = re.findall(reg, resp.text)[0][1]
                    charset = charset.lower()
                    resp.encoding = charset
                except:
                    resp.encoding = "utf-8"
                return resp.text
            else:
                return None
        except Exception as e:
            print(e)

    def set_parameter(self,url = None,headers= None,cookies = None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.html = self.getHtml()

    def get_contents(self ,X_path= None):
        contens = []
        try:
            for item in etree.HTML(str(self.html)).xpath(X_path):
                contens.append(str(item).strip())
        except:
            return contens
        return contens

if __name__ == '__main__':
    xpath = xPathTexts()
    xpath.set_parameter(url = "http://news.ifeng.com/c/7t2KBgHlEuW")
    print(xpath.get_contents('//p[@class= "author-3vIUPZtx"]//text()'))