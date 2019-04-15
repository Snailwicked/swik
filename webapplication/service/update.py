from dbs.sqliteclient import SqliteClient
import uuid

import datetime
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Update():

    def __init__(self):
        self.sqlite = SqliteClient()
    def update(self,parameter):
        update_sql = 'UPDATE web_info SET web_name = ?,web_url =? WHERE id = ? '
        data = [('{}'.format(parameter["web_name"]), '{}'.format(parameter["web_url"]),'{}'.format(parameter["id"]))]
        self.sqlite.update(update_sql,data)
        self.sqlite.close_all()

    def update_state(self, parameter):
        update_sql = 'UPDATE web_info SET state = ? WHERE id = ? '
        data = [('{}'.format(parameter["state"]), '{}'.format(parameter["id"]))]
        self.sqlite.update(update_sql, data)
        self.sqlite.close_all()