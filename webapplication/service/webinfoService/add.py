from db.client.sqliteclient import SqliteClient
import uuid

import datetime
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Add():

    def __init__(self):
        self.sqlite = SqliteClient()
    def add_one(self,parameter):
        save_sql = '''INSERT INTO web_info values (?, ?, ?,?,?)'''
        data = [('{}'.format(uuid.uuid1()), '{}'.format(parameter["web_name"]), '{}'.format(parameter["web_url"]),'{}'.format(nowTime),'0')]
        self.sqlite.save(save_sql,data)
        self.sqlite.close_all()

    def table(self):
        sql = '''CREATE TABLE `web_info` (`id` varchar(36) NOT NULL,
                                                              `url` varchar(200) NOT NULL,
                                                              `title` varchar(200) DEFAULT NULL,
                                                              `info` varchar(1000) DEFAULT NULL,
                                                              `time` varchar(10) DEFAULT NULL ,
                                                              `sentiment` int(10) DEFAULT NULL ,
                                                               PRIMARY KEY (`id`)
                                                            )'''

        self.sqlite.create_table(sql)
        self.sqlite.close_all()