import asyncio

from pprint import pprint

from core import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='a')
    url = AttrField(css_select='a', attr='href')


target_url = "http://news.sohu.com/"
loop = asyncio.get_event_loop()
items = loop.run_until_complete(HackerNewsItem.get_items(url=target_url))
pprint(items)