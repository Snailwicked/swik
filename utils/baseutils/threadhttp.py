import threading
import time
def fuction(parameters):
    print("parameters是json参数")
    '''
    这里书写你的爬虫程序
    '''

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
        crawler.start()
        self.crawlers.add(crawler)

    def join(self):
        for item in self.crawlers:
            item.join()




if __name__ == "__main__":

    runner = Crawlers()
    classification = ["bag", "shoes", "watch", "yifu", "shoushi"]
    for item in classification :
        runner.crawler(function,item)
    runner.join()
