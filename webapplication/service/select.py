from db.client.sqliteclient import SqliteClient

class Select():
    def __init__(self):
        self.sqlite = SqliteClient()
    def select_all(self):
        select_sql = '''select * from  web_info where \"state\" = 1 '''
        data = []

        for item in self.sqlite.fetchall(select_sql):
            model = {"id": "", "web_name": "", "web_url": "", "add_time": "", "state": ""}
            model["id"]= item[0]
            model["web_name"] = item[1]
            model["web_url"] = item[2]
            model["add_time"] = item[3]
            model["state"] = item[4]
            data.append(model)
        self.sqlite.close_all()
        return data
    def select_off(self):
        select_sql = "select * from  web_info where \"state\" = 0 "
        data = []
        for item in self.sqlite.fetchall(select_sql):
            model = {"id": "", "web_name": "", "web_url": "", "add_time": "", "state": ""}

            model["id"] = item[0]
            model["web_name"] = item[1]
            model["web_url"] = item[2]
            model["add_time"] = item[3]
            model["state"] = item[4]
            data.append(model)
        self.sqlite.close_all()
        return data
if __name__ == '__main__':
    select = Select()
    data = select.select_all()
    print(data)