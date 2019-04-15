from db.client.sqliteclient import SqliteClient
import uuid

import datetime
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Delete():

    def __init__(self):
        self.sqlite = SqliteClient()
    def delete_one(self,parameter):
        delete_sql = 'DELETE FROM web_info where web_url = ? and web_name=?'
        data = [('{}'.format(parameter["web_url"]),'{}'.format(parameter["web_name"]))]
        result = self.sqlite.delete(delete_sql,data)
        self.sqlite.close_all()
        return result

if __name__ == "__main__":
    delete =Delete()
    delete.delete_one({'id': '77852f88-40c3-11e9-a42d-9c5c8ed1c019', 'state': '0', 'add_time': '2019-03-07 18:26:16', 'web_url': '爱的是大所', 'web_name': '大萨达'})