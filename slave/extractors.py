# -*- coding: utf-8 -*-
import re
from lxml import etree
from dateutil.parser import parse as date_parser
import jieba
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import html as hl


class StringSplitter(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def split(self, string):
        if not string:
            return []
        return self.pattern.split(string)


class StringReplacement(object):
    def __init__(self, pattern, replaceWith):
        self.pattern = pattern
        self.replaceWith = replaceWith

    def replaceAll(self, string):
        if not string:
            return ''
        return string.replace(self.pattern, self.replaceWith)
def load_stopwords(path='../slave/stop_word'):
    with open(path, encoding="utf-8") as f:
        stopwords = list(map(lambda x: x.strip(), f.readlines()))
    stopwords.extend([' ', '\t', '\n'])
    return frozenset(stopwords)

MOTLEY_REPLACEMENT = StringReplacement("&#65533;", "")
ESCAPED_FRAGMENT_REPLACEMENT = StringReplacement(
    "#!", "?_escaped_fragment_=")
TITLE_REPLACEMENTS = StringReplacement("&raquo;", "»")
PIPE_SPLITTER = StringSplitter("\\|")
DASH_SPLITTER = StringSplitter(" - ")
UNDERSCORE_SPLITTER = StringSplitter("_")
SLASH_SPLITTER = StringSplitter("/")
ARROWS_SPLITTER = StringSplitter(" » ")
COLON_SPLITTER = StringSplitter(":")
SPACE_SPLITTER = StringSplitter(' ')
NO_STRINGS = set()
A_REL_TAG_SELECTOR = "a[rel=tag]"
A_HREF_TAG_SELECTOR = ("a[href*='/tag/'], a[href*='/tags/'], "
                       "a[href*='/topic/'], a[href*='?keyword=']")
RE_LANG = r'^[A-Za-z]{2}$'

good_paths = ['story', 'article', 'feature', 'featured', 'slides',
              'slideshow', 'gallery', 'news', 'video', 'media',
              'v', 'radio', 'press']
bad_chunks = ['careers', 'contact', 'about', 'faq', 'terms', 'privacy',
              'advert', 'preferences', 'feedback', 'info', 'browse', 'howto',
              'account', 'subscribe', 'donate', 'shop', 'admin']
bad_domains = ['amazon', 'doubleclick', 'twitter']

_STRICT_DATE_REGEX_PREFIX = r'(?<=\W)'
DATE_REGEX = r'([\./\-_]{0,1}(19|20)\d{2})[\./\-_]{0,1}(([0-3]{0,1}[0-9][\./\-_])|(\w{3,5}[\./\-_]))([0-3]{0,1}[0-9][\./\-]{0,1})?'
STRICT_DATE_REGEX = _STRICT_DATE_REGEX_PREFIX + DATE_REGEX

class ContentExtractor(object):
    def __init__(self,html = "",url = ""):

        self.doc = html
        self.url = url
    def get_authors(self):

        def uniqify_list(lst):

            seen = {}
            result = []
            for item in lst:
                if item != "":
                    if item.lower() in seen:
                        continue
                    seen[item.lower()] = 1
                    result.append(item.title())
            return result

        def parse_byline(search_str):
            # Remove HTML boilerplate
            search_str = re.sub('<[^<]+?>', '', search_str)
            # Remove original By statement
            search_str = re.sub('[bB][yY][\:\s]|[fF]rom[\:\s]', '', search_str)
            search_str = re.sub('written', '', search_str)


            search_str = search_str.strip()
            name_tokens = re.split("[^\w\'\-\.]", search_str)
            name_tokens = [s.strip() for s in name_tokens]

            _authors = []
            # List of first, last name tokens
            curname = []
            delimiters = ['and', ',', '']

            for token in name_tokens:
                if token in delimiters:
                    if len(curname) > 0:
                        _authors.append(' '.join(curname))
                        curname = []
                else:
                    curname.append(token)

            _authors.append(' '.join(curname))

            return _authors

        ATTRS = ['name', 'rel', 'itemprop', 'class', 'id','property']
        VALS = ['author', 'byline', 'dc.creator', 'byl','section','creator',]
        matches = []
        authors = []

        for attr in ATTRS:
            for val in VALS:
                found = etree.HTML(self.doc).xpath('//*[contains(@{0},"{1}")]'.format(attr, val))
                matches.extend(found)
        for match in matches:
            content = ''
            if match.tag == 'meta':
                mm = match.xpath('@content')
                if len(mm) > 0:
                    content = mm[0]
            else:
                result = etree.tostring(match)
                dr = re.compile(r'<[^>]+>', re.S)
                content = dr.sub('', result.decode('utf-8')) or ""

            if len(content) > 0:
                res = hl.unescape(content)
                authors.extend(parse_byline(res))

        if uniqify_list(authors):
            return uniqify_list(authors)[0]
        return ""

    def get_publishing_date(self):

        def parse_date_str(date_str):
            if date_str:
                try:
                    import time
                    return int(time.mktime(date_parser(date_str).timetuple())*1000)
                except (ValueError, OverflowError, AttributeError, TypeError):
                    # near all parse failures are due to URL dates without a day
                    # specifier, e.g. /2014/04/
                    regs = ['\d{2} \d{4} \d{2}:\d{2}:\d{2}','\d{4}-\d{2}-\d{2}@ \d{2}:\d{2}:\d{2}'.replace("@","")]  # 07 2019 09:52:53
                    result = []
                    for reg in regs:
                        result.extend(re.findall(reg, date_str))
                    if len(result) != 0:
                        return int(time.mktime(date_parser(result[0]).timetuple()) * 1000)
                    return ""

        date_match = re.search(STRICT_DATE_REGEX, self.url)
        if date_match:
            date_str = date_match.group(0)
            datetime_obj = parse_date_str(date_str)
            if datetime_obj:
                return datetime_obj

        ATTRS = ['property', 'name', 'itemprop', 'pubdate',"class","h6"]
        VALS = ['datePublished', 'published', 'PublicationDate', 'datePublished','published_time',
                'article_date', 'publication_date', 'sailthru.date', 'PublishDate', 'pubdate','dete','date','time']
        CONTENT = ["@content","@datetime","text()"]


        for attr in ATTRS:
            for val in VALS:
                for con in CONTENT:
                    found = etree.HTML(self.doc).xpath('//*[contains(@{0},"{1}")]//{2}'.format(attr, val,con))
                    if found:
                        for ti in found:
                            datetime_obj = parse_date_str(ti)
                            if str(datetime_obj)!="" and str(datetime_obj)[0]==1:
                                return datetime_obj
        return self.get_thirteenTime()


    def get_title(self):
        title = ''
        title_element = etree.HTML(self.doc).xpath('//title//text()')
        # no title found
        if title_element is None or len(title_element) == 0:
            return title
        # title elem found
        if len(title_element) != 0:
            title_text = title_element[0]
        else:
            title_text = ""
        used_delimeter = False

        title_text_h1 = ''
        title_text_h1_list =etree.HTML(self.doc).xpath('//h1//text()') or []

        if title_text_h1_list:
            title_text_h1_list.sort(key=len, reverse=True)
            title_text_h1 = title_text_h1_list[0]
            title_text_h1 = ' '.join([x for x in title_text_h1.split() if x])

        title_text_fb = (self.get_meta_content('//meta[@property="og:title"]') or self.get_meta_content('//meta[@name="og:title"]') or '')

        filter_regex = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9\ ]')
        filter_title_text = filter_regex.sub('', title_text).lower()
        filter_title_text_h1 = filter_regex.sub('', title_text_h1).lower()
        filter_title_text_fb = filter_regex.sub('', title_text_fb).lower()

        # check for better alternatives for title_text and possibly skip splitting
        if title_text_h1 == title_text:
            used_delimeter = True
        elif filter_title_text_h1 and filter_title_text_h1 == filter_title_text_fb:
            title_text = title_text_h1
            used_delimeter = True
        elif filter_title_text_h1 and filter_title_text_h1 in filter_title_text \
                and filter_title_text_fb and filter_title_text_fb in filter_title_text \
                and len(title_text_h1) > len(title_text_fb):
            title_text = title_text_h1
            used_delimeter = True
        elif filter_title_text_fb and filter_title_text_fb != filter_title_text \
                and filter_title_text.startswith(filter_title_text_fb):
            title_text = title_text_fb
            used_delimeter = True

        if not used_delimeter and '|' in title_text:
            title_text = self.split_title(title_text, PIPE_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        if not used_delimeter and '-' in title_text:
            title_text = self.split_title(title_text, DASH_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        if not used_delimeter and '_' in title_text:
            title_text = self.split_title(title_text, UNDERSCORE_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        if not used_delimeter and '/' in title_text:
            title_text = self.split_title(title_text, SLASH_SPLITTER,
                                          title_text_h1)
            used_delimeter = True

        if not used_delimeter and ' » ' in title_text:
            title_text = self.split_title(title_text, ARROWS_SPLITTER,
                                          title_text_h1)

        title = MOTLEY_REPLACEMENT.replaceAll(title_text)

        filter_title = filter_regex.sub('', title).lower()
        if filter_title_text_h1 == filter_title:
            title = title_text_h1
        return title.replace("\n","").strip()

    def split_title(self, title, splitter, hint=None):
        large_text_length = 0
        large_text_index = 0
        title_pieces = splitter.split(title)
        if hint:
            filter_regex = re.compile(r'[^a-zA-Z0-9\ ]')
            hint = filter_regex.sub('', hint).lower()
        for i, title_piece in enumerate(title_pieces):
            current = title_piece.strip()
            if hint and hint in filter_regex.sub('', current).lower():
                large_text_index = i
                break
            if len(current) > large_text_length:
                large_text_length = len(current)
                large_text_index = i
        title = title_pieces[large_text_index]
        return TITLE_REPLACEMENTS.replaceAll(title).strip()


    def get_meta_content(self, metaname):
        meta =etree.HTML(self.doc).xpath(metaname+"//@content")
        content = ""
        if meta is not None and len(meta) > 0:
            content = meta
        if content:
            return content[0].strip()
        return ''


    def get_content(self):

        reCOMM = '<!--.*?-->'
        reTRIM = '<{0}.*?>([\s\S]*?)<\/{0}>'
        reA = '<a>([\s\S]*?)<\/a>'
        reAS = '<a .*?>([\s\S]*?)<\/a>'

        text = re.sub(reCOMM, "", self.doc)
        text = re.sub(reTRIM.format("script"), "", re.sub(reTRIM.format("style"), "", text))
        text = re.sub(reTRIM.format("noscript"), "", re.sub(reTRIM.format("head"), "", text))
        text = re.sub(reA, "", re.sub(reTRIM.format("header"), "", text))
        text = re.sub(reAS, "", re.sub(reTRIM.format("header"), "", text))
        dr = re.compile(r'<[^>]+>', re.S)

        text = dr.sub('', text)

        ctexts = text.split("\n")
        textLens = [len(text) for text in ctexts]

        cblocks = [0] * (len(ctexts) -6)
        lines = len(ctexts)
        if lines>=6:
            for i in range(5):
                cblocks = list(map(lambda x, y: x + y, textLens[i: lines - 6 + i], cblocks))
            maxTextLen = max(cblocks)
            start = end = cblocks.index(maxTextLen)
            while start > 0 and cblocks[start] > min(textLens):
                start -= 1
            while end < lines - 6 and cblocks[end] > min(textLens):
                end += 1
            result = list(map(lambda string :self.fitlterWord(str(string).strip()),ctexts[start:end]))
            results="".join(list(map(lambda string:(string+"<br />") if len(string)>10 else (string) ,result)))
            return self.fitlterWord(results)
        else:
            result = "".join(ctexts)
            return self.fitlterWord(result)

    def fitlterWord(self,text):
        newtext=text.replace("&nbsp;", "").replace("&gt;", "").replace("&raquo;", "").strip()
        results = []
        regs = ["&#\d{4};",'&#\d{5};']
        for reg in regs:
            result = re.findall(reg, text)
            results.extend(result)
        for resu in results:
            newtext = newtext.replace(str(resu), "")
        return newtext


    def cut_sentence(self,sentence):

        delimiters = frozenset(u'。！？.?!')
        buf = []
        for ch in sentence:
            buf.append(ch)
            if delimiters.__contains__(ch):
                yield ''.join(buf)
                buf = []
        if buf:
            yield ''.join(buf)

    def get_summary(self,size=3):
        if self.get_meta_description() != "":
            return self.get_meta_description()
        else:
            docs = list(self.cut_sentence(self.get_content()))

            tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=load_stopwords())

            tfidf_matrix = tfidf_model.fit_transform(docs)

            normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)

            similarity = nx.from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)

            scores = nx.pagerank(similarity)

            tops = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            size = min(size, len(docs))

            indices = list(map(lambda x: x[0], tops))[:size]
            if len(str(list(map(lambda idx: docs[idx], indices))[0].strip()))>= 10:
                text = str(list(map(lambda idx: docs[idx], indices))[0].strip())
                return self.fitlterWord(text)
            return ""


    def get_meta_description(self):
        """If the article has meta description set in the source, use that
        """
        ATTRS = ['property', 'name', 'itemprop', 'pubdate', "class"]
        VALS = ['description']
        CONTENT = ["content"]
        result = []
        for attr in ATTRS:
            for val in VALS:
                for con in CONTENT:
                    found = etree.HTML(self.doc).xpath('//*[contains(@{0},"{1}")]//@{2}'.format(attr, val,con))
                    result.extend(found)
        resutlemns = list(map(lambda string :len(string),result))
        try:
            value=resutlemns.index(max(list(map(lambda string :len(string),result))))
        except:
            return ""

        if result[value]:
            return self.fitlterWord(str(result[value])).replace("&nbsp;","")
        return ""

    def get_uuid(self):
        def get_host_ip():
            try:
                import socket
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            finally:
                s.close()
            return ip
        struuid = "TT_{0}_8888_{1}_1".format(get_host_ip(), self.get_thirteenTime())
        return struuid

    def get_thirteenTime(self):
        import time
        millis = int(round(time.time() * 1000))
        return millis




if __name__ == "__main__":
    url = "http://www.sohu.com/a/302964777_115479"
    import requests
    res = requests.get(url)
    html = res.text
    charset = None
    try:
        reg = '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?'
        bianma = re.findall(reg, html)[0][1]
    except:
        bianma = ""
    if bianma != "":
        charset = bianma.lower()
    print(charset)
    res.encoding = charset



    ce = ContentExtractor(html=html,url=url)

    # print("发布时间",ce.get_publishing_date())
    # print("新闻标题",ce.get_title())
    print("新闻内容",ce.get_content())
    # print("新闻摘要",ce.get_summary())
    # print(ce.doc)
    # print(ce.get_uuid())
    # print(ce.get_thirteenTime())
    '''新闻内容 正文文章总阅读+1-->“端着个碗来大陆”，韩国瑜想要点什么<br />
       2019-03-22 08:03<br />
       来源://原标题：“端着个碗来大陆”，韩国瑜想要点什么<br />
       【文/观察者网专栏作家 雁默】<br />
       3月22日-28日，韩国瑜将访问大陆香港，澳门，深圳，厦门四城市，目的虽是城市间的经济文化交流，但由于韩目前在岛内人气颇高，甚至有呼声认为他很有可能成为台湾领导人，因此访陆、“访美”行都受到高度关注，各方眼睛都睁得很大。<br />
       
       据报载，有大陆网友认为韩这是“拿着碗来的”，那是当然，这位背负沉重债务的市长，拿着碗到处鞠躬哈腰求订单是职责所在，到大陆自然也是。为人民利益弯腰，是英雄行径，没什么好丢人的。
       
       <br />事实上，人还没去，高雄已获大批订单，分别是广东潮州连都贸易公司1年10亿元（新台币）订单，江苏文峰集团1年5亿订单，在韩上任八十几天后成为前三大订单的第一第二名。这几日还传出有澳门民企采购下了鲜花订单1年6600万，含在澳门51家供应商1年1.2亿的订单里。<br />
       
       戴着“财神帽”接受参访，韩国瑜表示要让高雄“发大财”（图片来源：东方IC）<br />韩国瑜的碗，现在满满是有形或无形的礼物，风光的是高雄人，丢人的则是欠下高额债务的陈菊，以及让县市首长不得不拿着碗到处弯腰，还予以嘲讽，打压，处处设限的民进党当局。<br />
       
       不过，对比于3000亿的债务，这些礼物仍是杯水车薪，高雄，乃至于整个台湾，需要的是大生意、大希望，韩国瑜仅以区区市长的地位，能做的却十分有限。仅凭高雄市长救不了高雄，韩国瑜若明年此时才领悟到这一点，就太晚了。<br />让我们先算算帐吧，台湾还有多少家底？<br />韩国瑜想在碗里放的是种子<br />所谓家底，就是外汇存底加上黄金储备。台湾黄金储备约为324公吨，约合台币3888亿，外汇存底约为4600亿美元，扣掉约92%的外资持有[注1]为368亿美元，约合台币1.14兆（万亿），两者相加就是约1.52兆，而“中央政府”每年总预算约为1.96兆。<br />换言之，台湾的家底还不足支应一年政府总预算，高雄市负债则占家底两成。<br />再者，外汇存底八到九成掌握在外资手里，而外资多数又以流动性最高的证券投资为主，倘若外资在短时间内大举撤离，台湾不死也只剩半条命。这意味着台湾必须为外资结构“整骨”。<br />台湾的外资结构是FPI（Foreign Portfolio Investment）远大于FDI（Foreign Direct Investment），FDI（外国直接投资）是指外国人将资金汇入台湾从事设备建置，厂房建造等长期性投资。FPI指的是投资组合，资金汇入台湾主要从事炒股、炒汇等短期性投资。<br />大白话来说，FDI是外国人比较愿意承担风险的投资“成本”，FPI是外国人见台湾情况好的时候一窝蜂涌进，不好的时候立马撤出的“赌本”。换言之，台湾外资结构是赌客居大多数，经营者却很少。<br />全球每年有约1.5兆美元的资金流动，香港往往可以抢到近千亿的份额，台湾则很少超过百亿。FDI不满百亿，FPI却高达两千亿美元，大家都是来赌的，乃台湾深重的经济问题。也就是说，台湾应该非常需要大幅提升FDI，从“九合一”选举时，民进党参选人陈其迈与韩国瑜都大喊要招商引资，即可得到明证。<br />台湾的FDI占GDP比重只有1.1%，可谓相当疲弱。诚然，FDI金额的高低，不必然与经济成长正相关，有些经济体如新加坡、香港的FDI占GDP的两成与近四成，韩国则只有0.7%，却同样都是经济成长相当亮眼的地区，荷兰的FDI占GDP高达三成五，但经济长期低靡。<br />台北市街景（图片来源：视觉中国）<br />显示FDI是否为经济体的主要成长来源，端视该经济体的取向是较重视本土产业发展，或是以外资为经济成长动力。星马显然属于后者，台湾、大陆都较倾向前者。<br />重点在于，台湾的本土产业与出口主力面临了瓶颈，正需要外资FDI注入活水，以作为经济结构调整的动力。这就是为什么韩国瑜近日重提马时期的“自由经济示范区”（自经区）计划，该计划事实上就是将眼光放在FDI，告别经济保守主义的政策，但自经区计划并未在马时期实现。<br />因此，韩国瑜访大陆四个城市，想放在碗里带回台湾的，是粤港澳大湾区以及“一带一路”这两粒真正具有长远价值的种子，借由这两粒种子的开花结果，既能为台湾经济整骨，也能深化两岸经贸与文化交流。其余订单或熊猫，都只是宣传意味比较高的小礼物。（高雄当然养得起熊猫，多的是企业会认养，这个问题应该从熊猫保育的角度来看，而不是财务负担。）<br />粤港澳大湾区以及“一带一路”的经济战略，大陆读者应该都非常熟悉了，但台湾民众知之甚少，韩国瑜的价值，就是能将其转化为庶民语言并较为有效地扫除路上的障碍。<br />设立自经区并与大陆经贸特区对接，能解决台湾签订FTA脚步落后而被边缘化的问题，当然政敌也会做出“鸡蛋放在同一个笼子里”的指责，但事实摆在眼前，绿营无法促成台湾加入CPTPP与RCEP，与美国签订FTA的希望也很渺茫，是根本连笼子都没有。<br />所以韩国瑜带着种子回台后，立刻就会进入政治内战。<br />2020年，有“匪气”者胜<br />在赖清德宣布参选后，民进党立刻陷入内战，但蔡赖之差别，仅在于85度C的“独”与100度C的“独”，无论谁胜出，都一样会打“危机牌”以求在2020年险中求胜。而就算落败，民进党也会力保40度C的“独”以图东山再起。<br />故而，今年蓝绿争胜是“经济牌”与“危机牌”的对决，蓝营的选战主轴，毫无疑问会套用韩国瑜的经济主张布局，无论参选人是谁。<br />现在绿营选民焦虑的是，应该离中间路线远一点或近一点，因为蔡赖已出现分歧。蓝营选民焦虑的是，推羔羊没有胜算，推土匪缺乏正当性。<br />赖清德与吴敦义（图片来源：东方IC）<br />羔羊者，国民党传统精英也，马，王，朱，吴皆此类，保守拘泥无战力。土匪者，韩国瑜也，接地气，敢突破，有勇有谋战力高。蓝营支持者盼了20年才出现一个有匪气的领袖抗击绿军，让战力高者困守一城，以羔羊做前锋，焦虑也很正常。<br />其实，韩国瑜参选当然能有正当性，而且十分简单，只需要将竞选主轴放在“让高雄成为台湾经济中心”即可，变成政治中心亦无不可，如此才真正能解决高雄问题。市长算什么？在一级政治高层里敬陪末座而已，而高雄确实病入膏肓，不下猛药难以根治。<br />高雄市确实有条件成为全岛经济中心，但绝非一个市长层级所能促成。<br />国民党“立委”与15位县市首长力推自经区救经济，虽然大方向正确，但做法缺乏谋略。马时期推动此政策之所以不了了之，就是因为放弃了从高雄做为起点的初衷，改采全台规模的“自由经济岛”，规划出“六海一空”（六个海港与一个空港，外加屏东生技园区）扩大架构。<br />由于各城市的背景不同，遇到的问题亦有差异，而自经区本来就是实验性质的计划，以台湾的政治环境来看，应该从小而大，以单一城市为起点，在不断调整修正的过程里逐步扩展至其他县市，才能有效避免事前规划上的虚耗。<br />之所以失败，除了绿营的杯葛，说到底，就是“蓝委”不团结，不团结，是因为各区域利益的矛盾，且知识显然不足。<br />举凡大计划，必须有一个意志力坚决的掌舵者主导，但马王问题使得国民党执政常常呈现双头马车，甚至有时马车对撞的现象，此乃蓝营之痼疾，也是绿营“拐马脚”常常能得逞的主因。君不见，民进党完全执政，想推什么法案就推什么法案，蓝营成功杯葛了什么案子吗？这不能全部推给席次不够，而是蓝营始终没有在内斗中孵出一个绝对领导人所致。<br />因此，韩国瑜应该记取之前的教训，趁着2020年“选举”有志角逐“立委”者都需要“韩流”的时机，统合出一个推动自经区的全台区域“立委”团队，形成一个土匪战力，方能因应绿营的“威胁牌”战术。<br />长期利益比短期抢救更重要<br />根据大陆商务部统计，台商投资大陆总额若加上第三地转投资，“实际使用台资”约1300亿美元。每年大陆来自台湾的投资额，不是第一名就是第二名，当香港是第一名的时候，港资中还包含许多以港商为名义投资大陆的台资。<br />反观大陆投资台湾的金额，由于台湾自己设下层层限制，所以自2009年开放陆资以来至今，总计只有近22亿美元。<br />视频网站“爱奇艺”进军台湾市场（图片来源：网络）<br />对台湾而言，经贸特区的意义之一，其实也是在法规上松绑，以吸引陆资与人才进驻，让两岸经贸交流往互利互赖的方向发展。<br />我一向不赞成政治让利，相信韩国瑜也不会认为这是正途，大架构下的经贸互利所能获得有形无形的效益，远远高于暂时性的让利。因此，当谢龙介在台南频频强调大陆订单时，我认为他可能低估了农民，短期抢救与长期利益，农渔民其实都看得清楚。多去解释大架构的经贸交流，能产生更有利于农渔民的产销结构，才是政策宣传的正确方向。<br />促成两岸经贸特区对接，没有人是土匪，两岸关系中的匪类，是人前说不要，人后偷偷在大陆捞钱的商业“台独”。<br />至于韩国瑜是否能在两岸政治协商里扮演推动的角色？那是另一个重要议题，观察重点在于国民党打两岸经济牌时，引起了什么样的各方互动，可随时事专文分析。<br />[注1] 外资持有台湾外汇存底的比例变动，常在85%-95%之间游移。<br />本文系观察者网独家稿件，未经授权，不得转载。      责任编辑：<br />声明：该文观点仅代表作者本人，搜狐号系信息发布平台，搜狐仅提供信息存储空间服务。<br />阅读 ()眼观六路耳听八方，域外西媒独家编译，境内热点犀利评论
       
       <br />观察者网app，满足你对资讯的卓越品味<br />
       推荐阅读今日搜狐热点6秒后今日推荐'''
