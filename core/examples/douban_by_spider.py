from core import AttrField, TextField, Item, Request,Middleware, Spider
from core.utils import get_random_user_agent

middleware = Middleware()

@middleware.response
async def print_on_response(request, response):
    print("实打实大萨达")
    # if response.callback_result:
    #     print(response.html)


class DoubanItem(Item):
    cover = AttrField(css_select='a', attr='href')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    start_urls = ['https://movie.douban.com/top250']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10
    async def parse(self, res):
        etree = res.e_html
        pages = ['?start=0&filter='] + [i.get('href') for i in etree.cssselect('.paginator>a')]
        headers = {
            "User-Agent": await get_random_user_agent()
        }
        for index, page in enumerate(pages):
            url = self.start_urls[0] + page
            yield Request(url,
                          request_config=self.request_config,
                          headers=headers,
                          callback=self.parse_item,
                          metadata={'index': index})

    async def parse_item(self, res):
        items_data = await DoubanItem.get_items(html=res.html)
        for item in items_data:
            print(item.cover)
        print(res)


if __name__ == '__main__':
    DoubanSpider.start(middleware=middleware)