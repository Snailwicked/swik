# -*- coding: utf-8 -*-
import redis

class RedisClient(object):


    def __init__(self):
        self.redis_conf = {'host': '101.132.113.50', 'port': 6379, 'encoding': 'utf-8', 'db': 0}
        self.__conn = redis.Redis(host=self.redis_conf['host'], port=self.redis_conf['port'], db=self.redis_conf['db'],
                                  encoding=self.redis_conf['encoding'])


    def add_urls(self,redis_key,start_urls):
        for url in start_urls:
            self.__conn.rpush(redis_key, url)


    def get_urlFromhead(self,redis_key):
        # value = None
        # while self.key:
        #     try:
        #         value = self.__conn.blpop(redis_key)
        #         self.key = 0
        #     except:
        #         self.key = 1
        #         import time
        #         time.sleep(60*60)
        value = self.__conn.blpop(redis_key)
        return value


    def get_urlSums(self,redis_key):
        # value = None
        # while self.key:
        #     try:
        #         value = self.__conn.llen(redis_key)
        #         self.key = 0
        #     except:
        #         self.key = 1
        #         import time
        #         time.sleep(60*60)
        value = self.__conn.llen(redis_key)
        return value


    def clear(self):

        self.__conn.flushdb()

if __name__ == '__main__':
    redis_con = RedisClient()
    # redis_con.put('abc')
    # redis_con.put('123')
    # redis_con.put('123.115.235.221:8800')
    # redis_con.put(['123', '115', '235.221:8800'])
    # print(redis_con.getAll())
    # redis_con.delete('abc')
    # print(redis_con.getAll())

    # print(redis_con.getAll())
    # redis_con.changeTable('test')
    # redis_con.pop()

    # redis_con.put('132.112.43.221:8888')
    # redis_con.changeTable('proxy')
    start_urls =['http://www.mitbbs.com/yimin/ymindex.php']
    # start_urls= ['http://www.ndtv.com', 'http://www.univarta.com', 'http://www.onlinekhabar.com', 'http://www.ratopati.com', 'http://headlinesindia.mapsofindia.com', 'http://radionepal.gov.np', 'https://thehimalayantimes.com', 'http://www.tribuneindia.com', 'http://www.indiandefensenews.in', 'https://www.nepalnational.com', 'http://www.bollywoodhungama.com', 'https://www.dailypioneer.com', 'http://www.businessbhutan.bt/businessbhutan', 'http://www.samacharjagat.com', 'http://www.dcnepal.com', 'http://www.patrika.com', 'https://hindi.news18.com', 'https://www.bhutantimes.com', 'http://www.indianexpress.com', 'http://firstpost.com', 'https://www.aljazeera.com/topics/country/nepal.html', 'http://m.dailyhunt.in/news', 'http://www.saharasamay.com', 'http://www.samaylive.com', 'http://hindi.oneindia.com', 'http://www.deccanherald.com', 'http://www.filmfare.com', 'https://www.in.com', 'http://nepalitimes.com', 'http://www.myrepublica.com', 'http://www.jansatta.com', 'http://www.telegraphindia.com', 'http://www.bhaskar.com', 'http://therisingnepal.org.np', 'http://www.jagran.com', 'http://www.bhutantoday.com.bt', 'http://www.amarujala.com', 'http://www.kuenselonline.com', 'http://www.outlookindia.com', 'http://www.freepressjournal.in', 'http://navbharattimes.indiatimes.com', 'https://www.indiancountrynews.com', 'http://www.prabhatkhabar.com', 'http://www.thenationalherald.com', 'http://nepaliheadlines.com', 'http://www.newsbullet.in', 'http://kathmandupost.ekantipur.com', 'http://www.deccanchronicle.com', 'https://thewire.in', 'https://www.indiatoday.in', 'http://www.business-standard.com', 'http://economictimes.indiatimes.com', 'http://www.esakal.com']
    # # for  urls in start_urls:
    # # print(urls)
    print(redis_con.get_urlSums("start_url"))
    # key = 1
    # while key :
    #     try:
    #         print()
    #         key = 0
    #     except:
    #         key = 1
    #         import time
    #         time.sleep(5)
    #         print("未链接到网络")
    # print(redis_con.getAll())
