import pymysql
from pymongo import MongoClient


class TaskSelect:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.client = MongoClient(host="101.132.113.50", port=27017)
        self.mongo_db = self.client["spider_manage"]
        self.task_config = self.mongo_db["task_config"]

    def select_task(self, data):
        print(data)
        page = int(data['page'])
        limit = int(data['limit'])
        status = str(data['status'])
        keyword = str(data['keyword'])

        if status=="":
            sql = "select * from spider_task where task_name like '%{}%'limit {}, {}".format (keyword,(page-1)*limit,limit)
            count_sql = "select * from spider_task where task_name like '%{}%'".format(keyword)
        else:
            sql = "select * from spider_task where status = {} and task_name like '%{}%' limit {}, {}".format(status,keyword,(page - 1) * limit, limit)
            count_sql = "select * from spider_task where status = {} and task_name like '%{}%'".format(status,keyword)
        cursors = self.db.cursor()
        try:
            cursors.execute(sql)
            data = cursors.fetchall()
            count = cursors.execute(count_sql)
            data = {'data': data, 'count': count}
            self.db.commit()
            return data
        except Exception as e:
            print(e)
        finally:
            self.db.close()

    def select_task_config(self, data):
        uuid = str(data['uuid'])
        result = self.task_config.find({"uuid": uuid}, {"_id": 0})
        return list(result)



if __name__ == '__main__':
    task = TaskSelect()
    data = {'keyword': '', 'status': '', 'page': '1', 'limit': '10'}
    for item in task.select_task(data).get("data"):
        print(item)