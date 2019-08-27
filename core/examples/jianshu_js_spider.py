from core import AttrField, TextField, Item, Spider

# from ruia import AttrField, TextField, Item, Spider
class JianshuItem(Item):
    target_item = TextField(css_select='ul.list>li')
    author_name = TextField(css_select='a.name')
    author_url = AttrField(attr='href', css_select='a.name')


class JianshuSpider(Spider):
    start_urls = ['https://nj.58.com/ershoufang/39157699356818x.shtml?putid=11863594']
    concurrency = 10
    # load_js = True

    async def parse(self, res):
        print(res.html)
        items = await JianshuItem.get_items(html=res.html)
        for item in items:
            print(item)


if __name__ == '__main__':
    JianshuSpider.start()