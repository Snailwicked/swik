# -*- coding: utf-8 -*-
import requests,re
from lxml import etree
'''
传入url,header通过xPath路径获取html中的数据
也可以直接传入html文档进行解析
url ,html 而选一即可
用法：
    url = "http://www.sohu.com/a/304311876_123753"
    
    html = '<ul> 
                <li class="cur" data-id=""><a href="javascript:void(0)"><em class="dot"></em>推荐</a></li>
                <li data-id="" data-tag-id="77953" ><a href="//search.sohu.com/?keyword=人才&queryType=outside">人才</a></li>
                <li data-id="" data-tag-id="77955" ><a href="//search.sohu.com/?keyword=户口&queryType=outside">户口</a></li>
                <li data-id="" data-tag-id="77954" ><a href="//search.sohu.com/?keyword=落户&queryType=outside">落户</a></li>
                <li data-id="" data-tag-id="77956" ><a href="//search.sohu.com/?keyword=人才计划&queryType=outside">人才计划</a></li>
                <li data-id="" data-tag-id="68487" ><a href="//search.sohu.com/?keyword=林宥嘉&queryType=outside">林宥嘉</a></li>
                <li data-id="" data-tag-id="77521" ><a href="//search.sohu.com/?keyword=要闻&queryType=outside">要闻</a></li>
                <li data-id="" data-tag-id="77589" ><a href="//search.sohu.com/?keyword=贸易战&queryType=outside">贸易战</a></li>
                <li data-id="" data-tag-id="77591" ><a href="//search.sohu.com/?keyword=特朗普&queryType=outside">特朗普</a></li>
                <li data-id="" data-tag-id="77590" ><a href="//search.sohu.com/?keyword=关税&queryType=outside">关税</a></li>
                <li data-id="" data-tag-id="78041" ><a href="//search.sohu.com/?keyword=股市&queryType=outside">股市</a></li>
                <li data-id="" data-tag-id="78040" ><a href="//search.sohu.com/?keyword=股票&queryType=outside">股票</a></li>
                <li data-id="" data-tag-id="78042" ><a href="//search.sohu.com/?keyword=世界杯&queryType=outside">世界杯</a></li>
            </ul>'
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
    def __init__(self, *args,**kwargs):
        self.html = None

    def getHtml(self,url = None,headers= None,cookies = None):
        '''
        获取self.url 的 html
        :return: html
        '''
        import time
        import random
        # pause_time = random.randint(1, 4)
        # time.sleep(pause_time)
        try:
            resp = requests.get(url=url,headers= headers ,cookies = cookies,timeout=30)
        except:
            pass
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

    def get_contents(self,html=None,url= None,headers=None,X_path= None,cookies = None):

        if html != None:
            self.html = html
        else:
            self.html = self.getHtml(url,headers,cookies)
        contens = []
        for item in etree.HTML(str(self.html)).xpath(X_path):
            contens.append(str(item).strip())
        return contens

if __name__ == "__main__":
    url = "http://www.sohu.com/a/304311876_123753"
    X_path= "//a//@href"
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',}

    xpt = xPathTexts()
    # html = '''<ul>     <li class="cur" data-id=""><a href="javascript:void(0)"><em class="dot"></em>推荐</a></li>
    #            <li data-id="" data-tag-id="77953" ><a href="//search.sohu.com/?keyword=人才&queryType=outside">人才</a></li>
    #             <li data-id="" data-tag-id="77955" ><a href="//search.sohu.com/?keyword=户口&queryType=outside">户口</a></li>
    #             <li data-id="" data-tag-id="77954" ><a href="//search.sohu.com/?keyword=落户&queryType=outside">落户</a></li>
    #             <li data-id="" data-tag-id="77956" ><a href="//search.sohu.com/?keyword=人才计划&queryType=outside">人才计划</a></li>
    #             <li data-id="" data-tag-id="68487" ><a href="//search.sohu.com/?keyword=林宥嘉&queryType=outside">林宥嘉</a></li>
    #             <li data-id="" data-tag-id="77521" ><a href="//search.sohu.com/?keyword=要闻&queryType=outside">要闻</a></li>
    #             <li data-id="" data-tag-id="77589" ><a href="//search.sohu.com/?keyword=贸易战&queryType=outside">贸易战</a></li>
    #             <li data-id="" data-tag-id="77591" ><a href="//search.sohu.com/?keyword=特朗普&queryType=outside">特朗普</a></li>
    #             <li data-id="" data-tag-id="77590" ><a href="//search.sohu.com/?keyword=关税&queryType=outside">关税</a></li>
    #             <li data-id="" data-tag-id="78041" ><a href="//search.sohu.com/?keyword=股市&queryType=outside">股市</a></li>
    #             <li data-id="" data-tag-id="78040" ><a href="//search.sohu.com/?keyword=股票&queryType=outside">股票</a></li>
    #             <li data-id="" data-tag-id="78042" ><a href="//search.sohu.com/?keyword=世界杯&queryType=outside">世界杯</a></li>
    #         </ul>'''
    contens = xpt.get_contents(url=url ,X_path=X_path,headers=headers)
    import requests
    for item in contens:
        print(item)