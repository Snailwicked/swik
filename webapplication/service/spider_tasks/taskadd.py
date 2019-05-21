import pymysql
import pymongo
import uuid
import datetime


class AddTask:
    def __init__(self):
        self.mysql_db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                                        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.mongo_db = pymongo.MongoClient("mongodb://101.132.113.50:27017/")

    def add_task(self, data):
        task_name = data['task_name']
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 0
        creater = 'admin'
        config_name = uuid.uuid3(uuid.NAMESPACE_DNS, create_time)
        cursors = self.mysql_db.cursor()
        try:
            sql = 'insert into spider_task(task_name, create_time, status, creater, config_name) values("%s", "%s", "%d", "%s", "%s")' % (task_name, create_time, status, creater, config_name)
            cursors.execute(sql)
            self.mysql_db.commit()
        except Exception as e:
            print(e)
        finally:
            self.mysql_db.close()
