# -*- coding: utf-8 -*-
import re
from lxml import etree
from dateutil.parser import parse as date_parser
import jieba
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import html as hl
from config.conf import get_algorithm
args = get_algorithm()

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
def load_stopwords(path=args["stop_word"]):
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
        VALS = ['author', 'byline', 'dc.creator', 'byl','section','creator','edit']
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
            for item in uniqify_list(authors):
                if "编" in item:
                    return item
            for item in uniqify_list(authors):

                if item.isdigit():
                    continue
                return item
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
        text = re.sub(reTRIM.format("SCRIPT"), "", re.sub(reTRIM.format("head"), "", text))
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
            results="".join(list(map(lambda string:(string+"<br /><br />") if len(string)>10 else (string) ,result)))
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
            docs = list(self.cut_sentence(str(self.get_content()).replace("<br />","")))

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
    url = "http://news.yznews.com.cn/2019-09/11/content_7066943.htm"
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
    res.encoding = charset

    html = res.text
    ce = ContentExtractor(html=html,url=url)

    # print("发布时间",ce.get_publishing_date())
    # print("新闻标题",ce.get_title())
    print("新闻内容",ce.get_content())
    # print("新闻摘要",ce.get_summary())
    # print("新闻作者",ce.get_authors())

    # print(ce.doc)
    # print(ce.get_uuid())
    # print(ce.get_thirteenTime())
