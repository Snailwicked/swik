import time
import re
import asyncio
import aiohttp
from collections import defaultdict
from urllib.parse import urljoin, urldefrag
from urllib.parse import unquote
from lxml import html
from core.headers import random_headers


class BQueue(asyncio.Queue):
    """ Bureaucratic queue """

    def __init__(self, maxsize=0, capacity=0, *, loop=None):
        """
        :param maxsize: a default maxsize from tornado.queues.Queue,
            means maximum queue members at the same time.
        :param capacity: means a quantity of income tries before will refuse
            accepting incoming data
        """
        super().__init__(maxsize, loop=None)
        if capacity is None:
            raise TypeError("capacity can't be None")

        if capacity < 0:
            raise ValueError("capacity can't be negative")

        self.capacity = capacity
        self.put_counter = 0
        self.is_reached = False

    def put_nowait(self, item):

        if not self.is_reached:
            super().put_nowait(item)
            self.put_counter += 1
            if 0 < self.capacity == self.put_counter:
                self.is_reached = True


class AWebSpider:

    def __init__(self, capture_pattern, concurrency=2, timeout=300,
                 delay=0,max_crawl=0, cookies=None,
                 start_url=None, retries=2):


        self.base = base_url
        self.start_url = start_url
        self.capture = re.compile(capture_pattern)
        self.exclude = [':']


        self.concurrency = concurrency
        self.timeout = timeout
        self.delay = delay
        self.retries = retries

        self.q_crawl = BQueue(capacity=max_crawl)
        self.q_parse = BQueue(capacity=max_crawl*100)

        self.brief = defaultdict(set)
        self.data = []

        self.can_parse = False

        if not cookies:
            cookies = dict()
        self.client = aiohttp.ClientSession(headers=random_headers, cookies=cookies)
        from urllib.parse import urlparse
        self.scheme = urlparse(self.start_url).netloc
    def get_parsed_content(self, url):
        """
        :param url: an url from which html will be parsed.
        :return: it has to return a dict with data.
        It must be a coroutine.
        """
        raise NotImplementedError

    def get_urls(self, document):
        urls = []
        urls_to_parse = []
        temp = set()
        dom = html.fromstring(document)
        [temp.add(item) for item in dom.xpath('//a/@href')]
        for href in temp:
            if any(e in href for e in self.exclude):
                continue
            url = unquote(urljoin(self.base, urldefrag(href)[0]))
            if self.capture.search(url):
                urls_to_parse.append(url)
            else:
                urls.append(url)
        return urls, urls_to_parse

    async def get_html_from_url(self, url):
        async with self.client.get(url) as response:
            if response.status != 200:
                pass
            return await response.text()

    async def get_links_from_url(self, url):
        document = await self.get_html_from_url(url)
        return self.get_urls(document)

    async def __wait(self, name):

        if self.delay > 0:
            self.log.info('{} waits for {} sec.'.format(name, self.delay))
            await asyncio.sleep(self.delay)

    async def crawl_url(self):
        current_url = await self.q_crawl.get()
        try:
            if self.scheme in current_url:
                if (current_url not in self.brief['crawled']) and (current_url not in self.brief['crawling']):
                    self.brief['crawling'].add(current_url)
                    urls, urls_to_parse = await self.get_links_from_url(current_url)
                    self.brief['crawled'].add(current_url)

                    for url in urls:
                        if self.q_crawl.is_reached:
                            break

                        if self.scheme in url:
                            if (url not in self.brief['crawled']) and (url not in self.brief['crawling']):


                                await self.q_crawl.put(url)
                            else:
                                pass
                        else:
                            pass

                    for url in urls_to_parse:
                        if self.q_parse.is_reached:
                            print('Maximum parse length has been reached')
                            break
                        if url not in self.brief['parsing']:
                            await self.q_parse.put(url)
                            self.brief['parsing'].add(url)

                    if not self.can_parse and self.q_parse.qsize() > 0:
                            self.can_parse = True
                else:
                    pass
            else:
                pass
        except Exception as exc:
            print('Exception {}:'.format(exc))

        finally:
            self.q_crawl.task_done()

    async def parse_url(self):
        url_to_parse = await self.q_parse.get()

        try:
            print(url_to_parse)

        except Exception:
            self.log.error('An error has occurred during parsing',
                           exc_info=True)
        finally:
            self.q_parse.task_done()

    async def crawler(self):
        while True:
            await self.crawl_url()
            await self.__wait('Crawler')

    async def parser(self):
        retries = self.retries
        while True:
            if self.can_parse:
                await self.parse_url()
            elif retries > 0:
                await asyncio.sleep(0.5)
                retries -= 1
            else:
                break
        return


    async def run(self):
        start = time.time()

        print('Start working')

        await self.q_crawl.put(self.start_url)

        def task_completed(future):

            exc = future.exception()
            if exc:
                self.log.error('Worker has finished with error: {} '
                               .format(exc), exc_info=True)

        tasks = []

        for _ in range(self.concurrency):
            fut_crawl = asyncio.ensure_future(self.crawler())
            fut_crawl.add_done_callback(task_completed)
            tasks.append(fut_crawl)
            fut_parse = asyncio.ensure_future(self.parser())
            fut_parse.add_done_callback(task_completed)
            tasks.append(fut_parse)

        await asyncio.wait_for(self.q_crawl.join(), self.timeout)
        await self.q_parse.join()

        for task in tasks:
            task.cancel()

        await self.client.close()

        end = time.time()
        print('Done in {} seconds'.format(end - start))

        assert self.brief['crawling'] == self.brief['crawled'], \
            'Crawling and crawled urls do not match'

        print('Total crawled: {}'.format(len(self.brief['crawled'])))
        print('Total parsing: {}'.format(len(self.brief['parsing'])))

        print('Total parsed: {}'.format(len(self.data)))

        print('Parsed data has been stored.')
        print('Task done!')

class Crawling:

    def __int__(self):
        self.parameters = None

    def set_parameters(self, parameters):
        self.parameters = parameters

    def run(self):
        start_url = 'http://www.sohu.com/'
        capture = 'http://www.sohu.com/a/\d+_\d+'
        max_crawl = 50
        web_crawler = AWebSpider(capture, max_crawl=max_crawl, start_url=start_url)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(web_crawler.run())
        finally:
            loop.close()

