from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from crawler.spiders.static_html import StaticNewsSpider
rules = [{"main_url":"http://www.tibetcy.com/","re_url":{"re0": "http://www.tibetcy.com/\w+.asp\?\w+_id=\d+"}}]
if __name__ == '__main__':
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    for rule in rules:
        runner.crawl(StaticNewsSpider, rule=rule)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()