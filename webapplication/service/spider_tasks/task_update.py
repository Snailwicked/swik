import pymysql
import pymongo


class TaskUpdate:
    def __init__(self):
        self.mysql_db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.mongo_db = pymongo.MongoClient("mongodb://101.132.113.50:27017/")

    def update_status(self, data):
        id = data['id']
        status = int(data['status'])
        sql = 'update spider_task set status=%d where id="%s"' % (status, id)
        cursors = self.mysql_db.cursor()
        try:
            cursors.execute(sql)
            self.mysql_db.commit()
        except Exception as e:
            print(e)
        finally:
            self.mysql_db.close()

    def query_mongo_urls(self, data):
        """
        首先要判断任务表中状态是否是开启的只有当是1才能调用
        :param data:
        :return:
        """
        id = data['id']
        sql = 'select config_name from spider_task where id="%s"' % id
        cursors = self.mysql_db.cursor()
        mongo = self.mongo_db.spider_manage.config
        try:
            cursors.execute(sql)
            config_name = cursors.fetchone()['config_name']
            urls = mongo.find_one({'uuid': config_name})['urls']
            return urls
        except Exception as e:
            print(e)
        finally:
            self.mysql_db.close()

    def update(self, data):
        """
        修改表格中部分可修改的数据如爬虫任务名称
        :param data:
        :return:
        """
        id = data['id']
        task_name = data['task_name']
        sql = 'update spider_task set task_name="%s" where id="%s"' % (task_name, id)
        cursors = self.mysql_db.cursor()
        try:
            cursors.execute(sql)
            self.mysql_db.commit()
        except Exception as e:
            print(e)
        finally:
            self.mysql_db.close()

