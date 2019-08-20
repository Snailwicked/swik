from core import Request


class LxmlLinkExtractor():


    def __int__(self):
        pass


    def get_url_xpath(self,url):
        yield Request(url=url).fetch()


if __name__ == '__main__':
    LxmlLinkExtractor