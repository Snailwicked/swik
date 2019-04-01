import threading
import time
from spiders.xinshang import function

class oneThread(threading.Thread):
    def __init__(self, fuction,parameters):
        threading.Thread.__init__(self,)
        self.fuction = fuction
        self.parameters = parameters

    def run(self):
        self.fuction(self.parameters)


class Crawlers():

    def __init__(self):
        self.crawlers = set()

    def crawler(self,fuction,parameters):
        crawler = oneThread(fuction,parameters)
        self.crawlers.add(crawler)

    def start(self):
        for item in self.crawlers:
            item.start()




if __name__ == "__main__":

    runner = Crawlers()
    classification = ["bag", "shoes", "watch", "yifu", "shoushi"]
    for item in classification :
        runner.crawler(function,item)
    runner.start()