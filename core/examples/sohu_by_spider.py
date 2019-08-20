import aiofiles

from core import AttrField, TextField, Item, Spider

class HackerNewsItem(Item):
    target_item = TextField(css_select='a')
    url = AttrField(css_select='a', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['http://news.sohu.com/', 'http://www.sohu.com/']

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            self.start_urls.append(item.url)

            print(item.url)


if __name__ == '__main__':
    HackerNewsSpider.start()