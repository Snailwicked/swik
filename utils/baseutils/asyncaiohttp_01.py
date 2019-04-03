import asyncio
import re
import urllib.parse
import aiohttp

class Crawler:
    def __init__(self, rooturl, loop, maxtasks=100):
        self.rooturl = rooturl
        self.loop = loop
        self.todo = set()
        self.busy = set()
        self.done = {}
        self.tasks = set()
        self.htmls = set()
        self.sem = asyncio.Semaphore(maxtasks, loop=loop)
        self.session = aiohttp.ClientSession(loop=loop)

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
    def addhtmls(self, url ,html):
        print(len(self.htmls),'data:', (url ,html))
        self.htmls.add((url ,html))

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
                data = (yield from resp.read()).decode('utf-8', 'replace')
                urls = re.findall(r'(?i)href=["\']?([^\s"\'<>]+)', data)
                asyncio.ensure_future(self.addhtmls(url,data), loop=self.loop)
                asyncio.Task(self.addurls([(u, url) for u in urls]))

            resp.close()
            self.done[url] = True
        self.busy.remove(url)
        print(len(self.done), 'completed tasks,', len(self.tasks),
              'still pending, todo', len(self.todo))


def main():
    loop = asyncio.get_event_loop()

    c = Crawler("http://news.sohu.com/", loop)
    asyncio.ensure_future(c.run(), loop=loop)
    try:
        loop.run_forever()
    finally:
        loop.close()
    print('todo:', len(c.todo))
    print('busy:', len(c.busy))
    print('done:', len(c.done), '; ok:', sum(c.done.values()))
    print('tasks:', len(c.tasks))
if __name__ == '__main__':
    main()






