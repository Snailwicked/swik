import time
import asyncio
import threading
import requests
url = "http://91xinshang.com/xianzhi/NGQ2Z05JZWtwVVU9.html"
def run3():
    for i in range(5):
        html = requests.get(url).text
        print("同步代码",time.time())

class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.function()
    def function(self):
        html = requests.get(url).text
        print("线程代码",time.time())


def run2():
    thread1 = myThread()
    thread2 = myThread()
    thread3 = myThread()
    thread4 = myThread()
    thread5 = myThread()
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

# async def hello():
#     html = requests.get(url).text
#     print('异步代码:%s' % time.time())
#
# def run():
#     for i in range(5):
#         loop.run_until_complete(hello())
# loop = asyncio.get_event_loop()


class myThread2(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.function = name

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        try:
            self.function()
        except:
            pass

if __name__ =='__main__':
    my2 = myThread2(run2())
    # my3 = myThread2(run())
    my1 = myThread2(run3())
    my1.start()
    my2.start()
    # my3.start()


