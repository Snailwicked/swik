import asyncio
import re
import urllib.parse
import aiohttp
import queue


class queueUtil:
    def __init__(self):
        self.queue = queue.Queue()

    def put(self,data):
        self.queue.put(data)
    def get(self):
        while not self.queue.empty():
            if self.queue.qsize()<10:
                import time
                time.sleep(5)
            yield self.queue.get()



class Crawler:
    def __init__(self, maxtasks=100):
        self.rooturl = None
        self.loop = None
        self.todo = set()
        self.busy = set()
        self.done = {}
        self.tasks = set()
        self.sem = asyncio.Semaphore(maxtasks, loop=self.loop)
        self.session = aiohttp.ClientSession(loop=self.loop)

    @asyncio.coroutine
    def run(self):
        t = asyncio.ensure_future(self.addurls([(self.rooturl, '')]),
                                  loop=self.loop)
        yield from asyncio.sleep(1, loop=self.loop)
        while self.busy:
            yield from asyncio.sleep(1, loop=self.loop)

        yield from t
        yield from self.session.close()
        self.loop.stop()

    @asyncio.coroutine
    def addurls(self, urls):
        for url, parenturl in urls:
            url = urllib.parse.urljoin(parenturl, url)
            url, frag = urllib.parse.urldefrag(url)
            if (url.startswith(self.rooturl) and
                    url not in self.busy and
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
        # print('processing:', url)

        self.todo.remove(url)
        self.busy.add(url)
        try:
            resp = yield from self.session.get(url)
        except Exception as exc:
            print('...', url, 'has error', repr(str(exc)))
            self.done[url] = False
        else:
            if (resp.status == 200 and
                    ('text/html' in resp.headers.get('content-type'))):
                html = (yield from resp.read())
                data = html.decode('utf-8', 'replace')

                urls = re.findall(r'(?i)href=["\']?([^\s"\'<>]+)', data)
                asyncio.Task(self.addurls([(u, url) for u in urls]))
                try:
                    reg = '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?'
                    charset = re.findall(reg,data)[0][1]
                except:
                    charset = ""
                if charset != "":
                    charset = charset.lower()
                else:
                    charset = "utf-8"
                data = html.decode(charset, 'replace')

                asyncio.ensure_future(self.response((url,data)), loop=self.loop)

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
        print('data:DSADA', item)


    def main(self,loop):
        self.rooturl = "http://news.sohu.com/"
        self.loop = loop

        tasks = asyncio.gather(  # gather() 可以将一些 future 和协程封装成一个 future
            asyncio.ensure_future(self.run(), loop=loop),# ensure_future() 可以将一个协程封装成一个 Task
        )
        return tasks

    def start(self):
        loop = asyncio.get_event_loop()

        loop.run_until_complete(self.main(loop))
        loop.close()


if __name__ == '__main__':
    crawler = Crawleruning()
    crawler.start()








