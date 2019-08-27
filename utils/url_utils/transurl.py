import re
'''
判断是否为新闻的几个条件
一 包含时间的url基本为新闻
二 包含 html  shtml htm等多半为新闻
三 包含 list index page /？ /# 等基本不是新闻
四 以“/ com  cn”结尾的基本不是新闻
五 包含一大串数字的多半是新闻
'''


class transUrl():
    def __init__(self):
        self.newurl = ""
    def befor(self):
        '''
        去除约束，域名
        :return:
        '''
        import urllib.parse
        result = urllib.parse.urlparse(self.url)
        uselessStr = result.scheme + "://" + result.netloc
        self.url = self.url.replace(uselessStr, "")
        if self.url =="" or self.url[0:-1] == "":
            return "/notnews"
        return ""

    def have_time(self):
        '''
        判断url是否包含时间
        :param url:
        :return:/2018-03-15/,/2018_03_15/,/2018-03/15/,/2018-03/,/2018/03/15/,/2018/0315/,/20180315/
        '''
        regexis = [r'20\d{2}-\d{2}-\d{2}',r'20\d{2}_\d{2}_\d{2}/',r'20\d{2}-\d{2}/\d{2}/', r'20\d{2}-\d{2}/',
                         r'20\d{2}/\d{2}/\d{2}/', r'20\d{2}/\d{4}/', r'20\d{6}/','20\d{2}/\d{2}/']
        results = []
        for regexi in regexis:
            result = re.findall(regexi, self.url)
            results.extend(result)
        if results != []:
            for key in results:
                self.url = self.url.replace(key, "")
            return "/isnews"
        return ""


    def seriesnums(self):
        regs = ["\d{8}","\d{7}","\d{6}","\d{5}","\d{4}"]
        results = []
        for reg in regs:
            result = re.findall(reg, self.url)
            results.extend(result)
        if results!=[]:
            for key in results:
                self.url = self.url.replace(key, "")
            return "/havenums"
        return ""

    def sumsspilt(self):
        '''
            判断新闻url中 " - "的数量，数量大于等于5基本上是新闻小于5可能是新闻
            :param url:
            :return:
        '''

        regs = ["\w+\----", "\w+\---", "\w+\--", "\w+\-","\w+\+","\w+\-"]
        results = []
        for reg in regs:
            result = re.findall(reg, self.url)
            results.extend(result)
        if results != []:
            for key in results:
                self.url = self.url.replace(key, "")
            if len(results) >= 5:
                return "/isnews"
            return "/maybenews"
        return ""

    def snotnews(self):
        '''
        判断 list 404 page index 是否存在在url中
        :param url:
        :return:
        '''
        list_str = ['list','index','404','page','login','category','jpg',"pdf"]
        old = self.spilt_url()
        for str_one in list_str:
            for elememt in str(self.url).split("/"):
                if str_one in elememt:
                    self.url = self.url.replace(elememt, "")
        if len(old) != len(self.url):
            return "/noturl"
        return ""

    def spilt_url(self):
        '''
        尝试将url进行分词处理 按照 / 切分
        :param url:
        :return: 是一个str类型  如'a b c dd e'
        '''
        self.url = self.url.replace('.','/')
        self.url = self.url.replace('_','/')
        self.url = self.url.replace('-','/')
        self.url = self.url.replace('=','/')
        self.url = self.url.replace('?','/')
        self.url = self.url.replace('/?','/')
        self.url = self.url.replace('&','/')
        self.url = self.url.replace('#','/')
        return self.url

    def get_feature(self,url):
        self.url = url
        befor = self.befor()
        havetime = self.have_time()
        sumsspilt = self.sumsspilt()
        seriesnums = self.seriesnums()
        snotnews = self.snotnews()
        result = self.spilt_url() + befor + havetime + sumsspilt + snotnews + seriesnums
        return result


class transUrls(transUrl):
    def __init__(self):
        super(transUrls, self).__init__()

    def transport(self,urls):
        results = []
        for url in urls :
            result = self.get_feature(url)
            results.append(result)
        return results
if __name__ == '__main__':
    url = {'http://lady.163.com', 'http://money.163.com/19/0325/14/EB4DVVP3002581PP.html',
     'http://money.163.com/19/0321/07/EAPC44EO00258J1R.html', 'http://money.163.com/19/0325/15/EB4G7359002580S6.html',
     'http://v.163.com/static/3/VK2ILS3FP.html', 'http://money.163.com/yanbao', 'http://lady.163.com/astro',
     'http://sitemap.163.com/', 'http://money.163.com/special/stock190325/',
     'http://lady.163.com/sense', 'http://money.163.com/18/1113/15/E0GK0E4100259C1M.html', 'https://news.163.com/',
     'http://m.163.com/newsapp/#f=topnav', 'http://jingdian.travel.163.com/domestic/1000066926/#f=endnav',
     'http://email.163.com/', 'http://haoma.163.com', 'http://money.163.com/special/002530GG/special.html',
     'http://money.163.com/19/0105/20/E4PJTG5S00259CBS.html', 'http://money.163.com/kechuangban/',
     'http://money.163.com/photoview/0BGT0025/27117.html', 'https://epay.163.com/', 'http://money.163.com/latest/ ',
     'http://money.163.com/special/wangyiyanjiujudashi/', 'http://quotes.money.163.com/forex/hq/USDHKD.html#1b01',
     'http://jingdian.travel.163.com', 'http://money.163.com/19/0322/23/EATJGOKN00259ARN.html',
     'http://xf.house.163.com', 'http://money.163.com/19/0325/16/EB4IU5L3002581PP.html',
     'http://money.163.com/17/0810/14/CRG0TO380025984C.html', 'http://money.163.com/19/0322/07/EART8PO300258J1R.html',
     'http://v.163.com/static/3/VK33Q3V08.html', 'http://ent.163.com', 'http://house.163.com/',
     'http://money.163.com/19/0325/08/EB3POVNO002580S6.html',
     'http://money.163.com/photoview/HP480025/31497.html#p=CRGAU623HP480025NOS',
     'http://v.163.com/static/3/VK5U6G8FI.html', 'http://auto.163.com/depreciate',
     'http://money.163.com/17/1218/10/D5UALF9V002599JF.html', 'http://money.163.com/19/0307/08/E9LD1LQL00258J1R.html',
     'http://money.163.com/hkstock/', 'http://money.163.com/special/00pai-2/', 'http://ent.163.com/special/xbkhz/',
     'http://money.163.com/usstock', 'http://money.163.com/19/0315/07/EA9RF91200259C5R.html',
     'http://sports.163.com/nba', 'http://i.money.163.com/fundmall/', 'http://news.163.com/world',
     'http://www.stcn.com', 'http://study.163.com/?utm_source=163.com&utm_medium=web_bottomlogo&utm_campaign=business',
     'http://caipiao.163.com/#from=dh', 'http://www.yicai.com/', 'http://edu.163.com/special/official',
     'http://money.163.com/stock', 'http://cosmetic.lady.163.com/trial', 'http://quotes.money.163.com/stock#1b01',
     'http://www.163.com/rss',
     'http://rd.da.netease.com/redirect?t=KApRocvHmn&p=NNOB1N&proId=1922&target=http%3A%2F%2Fwww.kaola.com%2Factivity%2Fdetail%2F12026.shtml%3Ftag%3Dbe3d8d027a530881037ef01d304eb505',
     'http://money.163.com/special/00252G50/macro.html', 'http://money.163.com/18/0827/18/DQ82PQQ000258105.html',
     'http://money.163.com/18/0827/17/DQ807O0400259BF2.html', 'https://c.m.163.com/news/s/S1553477154337.html',
     'http://sports.163.com/yc', 'http://daxue.163.com', 'http://money.163.com/15/1214/15/BAQBUH5J002556Q4.html',
     'http://money.163.com/19/0322/08/EARVRGIH00258J1R.html', 'http://www.163.com/',
     'http://v.163.com/static/1/VK3RQNP01.html', 'http://money.163.com/photoview/0BGT0025/34815.html',
     'http://www.cs.com.cn/', 'http://quotes.money.163.com/old/#FN',
     'http://money.163.com/special/00253368/institutions.html', 'http://money.163.com/19/0322/07/EARTBQQC00259ARN.html',
     'http://money.163.com/special/2019davos/', 'http://money.163.com/19/0325/15/EB4HBSK6002581PP.html',
     'http://money.163.com/special/2017naecsummer/', 'http://money.163.com/blog/',
     'http://money.163.com/photoview/6V240025/27118.html', 'http://u.163.com/aosoutbdbd8',
     'http://quotes.money.163.com/hkstock/HSCCI.html#1b01', 'http://money.163.com/15/0725/11/AVC89MBU00252G50.html',
     'http://quotes.money.163.com/hkstock/HSI.html#1b01', 'http://v.163.com/static/3/VK2I2CPCG.html',
     'http://sports.163.com', 'http://dy.163.com/v2/media/homepage/T1486537600008.html',
     'http://money.163.com/19/0308/07/E9NRKDBK00259BNT.html', 'http://v.163.com/static/1/VK52NMU5R.html',
     'http://quotes.money.163.com/stock/#FN', 'http://quotes.money.163.com/old/#query=gjqz',
     'http://sports.163.com/world', 'http://money.163.com/fund/',
     'http://dy.163.com/v2/media/homepage/T1507526438958.html', 'http://money.163.com/18/1113/14/E0GH701S00259C1M.html',
     'https://www.lmlc.com/web/activity/bind_index.html?from=tgn163dh2', 'http://news.163.com/photo',
     'http://study.163.com/client/download.htm?from=163app&utm_source=163.com&utm_medium=web_app&utm_campaign=business',
     'http://chinese.wsj.com/gb/index.asp', 'http://www.ccstock.cn/', 'http://jiankang.163.com/',
     'http://money.163.com/finance', 'http://money.163.com/19/0325/15/EB4I1V5A002581PP.html',
     'http://money.163.com/latest/', 'http://money.163.com/special/2018naecsummerxx/', 'http://digi.163.com/smart',
     'http://hea.163.com/', 'http://jubao.aq.163.com/', 'http://money.163.com/chinext',
     'http://v.163.com/special/video/#tuijian', 'http://money.163.com/16/1214/13/C88FOA5B00258BVI.html',
     'http://ecard.163.com/script/index#f=topnav', 'http://money.163.com/19/0105/12/E4ON4CTB00259CBS.html',
     'http://auto.163.com/photo', 'http://money.163.com/photoview/0BGT0025/34814.html', 'http://www.aastocks.com.cn',
     'http://www.lczb.net/', 'http://reg.email.163.com/unireg/call.do?cmd=register.entrance&flow=mobile&from=ntes_nav',
     'http://v.mobile.163.com', 'http://product.auto.163.com/finder', 'http://cn.reuters.com/',
     'http://www.iceo.com.cn/', 'http://ent.163.com/special/gsbjb/', 'http://money.163.com/stock/',
     'http://money.163.com/17/0810/11/CRFMUVF80025984C.html', 'http://money.163.com/17/0810/12/CRFPSNQK0025984C.html',
     'http://corp.163.com/'}
    uu =transUrls()
    print(uu.transport(url))