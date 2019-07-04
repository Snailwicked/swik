
from pymongo import MongoClient

class TaskConfigUpdate:

    def __init__(self):
        self.client = MongoClient(host="101.132.113.50", port=27017)
        self.mongo_db = self.client["spider_manage"]
        self.task_config = self.mongo_db["task_config"]

    def update(self,data):
        uuid = str(data["uuid"])
        urls = eval(data["urls"])

        print(uuid)
        self.task_config.update({"uuid":uuid},{'$set':{'urls':urls}})
        return "0"

if __name__ == '__main__':
    taskconfig = TaskConfigUpdate()
    data = {"uuid":"bd029a52-54bf-31c4-9461-53e6d13d5224"}
    taskconfig.update(data)