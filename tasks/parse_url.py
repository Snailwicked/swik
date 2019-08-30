from db.redis_db import Url_Parameter
url_storage = Url_Parameter()
def parse_url():
    while True:
        parameters = url_storage.fetch_parameters("新闻爬虫")
        if parameters:
            for item in parameters:
                print(item)
        elif len(parameters)<5:
            break

parse_url()