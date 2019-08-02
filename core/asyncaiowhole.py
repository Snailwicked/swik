import asyncio
import re
import urllib.parse
import aiohttp
from lxml import etree
from urllib.parse import urljoin
from core.headers import random_headers




class Crawler:
    def __init__(self, maxtasks=100):
        self.loop = None
        self.todo = set()
        self.busy = set()
        self.done = {}
        self.tasks = set()
        self.sem = asyncio.Semaphore(maxtasks, loop=self.loop)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.dataset = set()
        self.parameter = None

    @asyncio.coroutine
    def run(self):
        t = asyncio.ensure_future(self.addurls([(self.parameter['url'], '')]),
                                  loop=self.loop)
        tas = []
        tas.append(t)
        yield from asyncio.sleep(1, loop=self.loop)
        while self.busy:
            yield from asyncio.sleep(1, loop=self.loop)
        yield from self.session.close()

        yield from tas
        self.loop.stop()

    @asyncio.coroutine
    def addurls(self, urls):
        for url, parenturl in urls:
            url = urllib.parse.urljoin(parenturl, url)
            url, frag = urllib.parse.urldefrag(url)
            if (url not in self.busy and
                    url not in self.done and
                    url not in self.todo):
                self.todo.add(url)
                yield from self.sem.acquire()
                task = asyncio.ensure_future(self.process(url), loop=self.loop)
                task.add_done_callback(lambda t: self.sem.release())
                task.add_done_callback(self.tasks.remove)
                self.tasks.add(task)

    @asyncio.coroutine
    def response(self, item):
        pass

    @asyncio.coroutine
    def process(self, url):

        self.todo.remove(url)
        self.busy.add(url)
        try:
            resp = yield from self.session.get(url,headers=random_headers)
        except Exception as exc:
            print('...', url, 'has error', repr(str(exc)))
            self.done[url] = False
        else:
            if (resp.status == 200):
                html = (yield from resp.read())
                data = html.decode('utf-8', 'replace')
                try:
                    reg = '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?'
                    charset = re.findall(reg,data)[0][1]
                except:
                    charset = "utf-8"
                data = html.decode(charset.lower(), 'replace')

                try:
                        for item in etree.HTML(str(data)).xpath("//a//@href"):
                                suburl = urljoin(url, item)
                                if suburl.startswith("http"):
                                        if suburl not in self.dataset:
                                                self.dataset.add(suburl)
                                                asyncio.ensure_future(self.addurls([(suburl, url)]), loop=self.loop)
                                        else:
                                                continue
                except:
                        pass
                result = re.findall(self.parameter['re_Rule'], url)
                if result:
                        asyncio.ensure_future(self.response((url)), loop=self.loop)
                else:
                        pass
            resp.close()
            self.done[url] = True
        self.busy.remove(url)
        print(len(self.done), 'completed tasks,', len(self.tasks),
              'still pending, todo', len(self.todo))


class Crawleruning(Crawler):

    def __init__(self):
        super(Crawleruning, self).__init__()

    @asyncio.coroutine
    def response(self, item):
        print(item)


    def main(self,loop):


        self.loop = loop

        tasks = asyncio.gather(  # gather() 可以将一些 future 和协程封装成一个 future
            asyncio.ensure_future(self.run(), loop=loop),# ensure_future() 可以将一个协程封装成一个 Task
        )
        return tasks

    def start(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.main(loop))
        except:
            loop.close()

    def set_parameter(self,parameter):
        self.parameter = parameter


if __name__ == '__main__':
    parameter = {
        "url": "http://news.sohu.com/",
        "re_Rule": "http://www.sohu.com/a/\d+_\d+"
    }
    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()








