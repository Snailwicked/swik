import asyncio
from aiohttp import ClientSession
import re

class ASymain():

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        self.charset = "utf-8"

    async def getHTML(self,url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    reg = '<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?'
                    bianma = re.findall(reg, await response.text())[0][1]
                except:
                    bianma = ""
                if bianma != "":
                    self.charset = bianma.lower()
                print(self.charset)
                response.encoding = self.charset
                try:
                    return await response.text()
                except:
                    print("pass")
    def run(self,urls):
        for url in urls:
            task = asyncio.ensure_future(self.getHTML(url))
            self.tasks.append(task)
        yield self.loop.run_until_complete(asyncio.gather(*self.tasks))

    def start(self,urls):
        self.loop = asyncio.get_event_loop()
        for item in self.run(urls):
            print(item)





if __name__ == '__main__':
    urls = ["http://news.sohu.com/","",""]

    am =ASymain()
    am.start(urls)
