import re

#传入多个xpath，哪个有内容返回哪个
def parse_content(html,xpath_rule):
    for xpath in xpath_rule:
        account_nickname_list = html.xpath(xpath)
        if len(account_nickname_list):
            return account_nickname_list[0]


#移除标签
def removehtml(html):
    p = re.compile('<[^>]+>')
    return p.sub("", html)
