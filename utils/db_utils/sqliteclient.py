import sqlite3
import os


class SqliteClient(object):

    def __init__(self):
        self.DB_FILE_PATH = "spider.db"
        self.show_sql = True
        self.conn = self.get_conn()
        self.cu = self.get_cursor()
        self.one_info = None


    def get_conn(self):
        '''该方法是建立数据库的连接，系统默认数据库名
           称为spider.db，如果存在该数据库则建立连接，不
           存在则新建一个名为spider.db的数据库且在新数据
           库中创建web_info表'''
        if os.path.exists(self.DB_FILE_PATH) and os.path.isfile(self.DB_FILE_PATH):
            return sqlite3.connect(self.DB_FILE_PATH)
        else:
            file = open(self.DB_FILE_PATH, 'w')
            file.close()
            conn = sqlite3.connect(self.DB_FILE_PATH)
            create_table_sql = '''CREATE TABLE `web_info` (
                                                              `id` varchar(36) NOT NULL,
                                                              `web_name` varchar(50) NOT NULL,
                                                              `web_url` varchar(200) DEFAULT NULL,
                                                              `language` varchar(11) DEFAULT NULL,
                                                              `proxy` int(10) DEFAULT 0,
                                                              `state` int(10) DEFAULT 0,
                                                               PRIMARY KEY (`id`)
                                                            )'''
            if self.show_sql:
                print('执行sql:[{}]'.format(create_table_sql))
            cu = conn.cursor()
            cu.execute(create_table_sql)
            conn.commit()
            print('创建数据库表[student]成功!')
            cu.close()
            return conn

    def get_cursor(self):
          '''该方法是获取数据库的游标对象，参数为数据库的连接对象
          如果数据库的连接对象不为None，则返回数据库连接对象所创
          建的游标对象；否则返回一个游标对象，该对象是内存中数据
          库连接对象所创建的游标对象'''
          if self.conn is not None:
              return self.conn.cursor()
          else:
              return sqlite3.connect('').cursor()


    def drop_table(self,table):
        '''删除数据库中的表'''

        sql = 'DROP TABLE IF EXISTS {}'.format(table)

        if table is not None and table != '':
            if self.show_sql:
                print('执行sql:[{}]'.format(sql))
            self.cu.execute(sql)
            self.conn.commit()
            print('删除数据库表[{}]成功!'.format(table))
        else:
            print('the [{}] is empty or equal None!'.format(sql))



    def create_table(self, sql):
        if sql is not None and sql != '':
            if self.show_sql:
                print('执行sql:[{}]'.format(sql))
            self.cu.execute(sql)
            self.conn.commit()
            print('创建数据库表[student]成功!')
        else:
            print('the [{}] is empty or equal None!'.format(sql))


    def fetchall_table(self):
        sql = "select name from sqlite_master where type='table' order by name"
        if self.show_sql:
            print('执行sql:[{}]'.format(sql))
        tables =self.cu.execute(sql)
        for info in tables:
            print(info[0])
        self.conn.commit()
        return tables


    def table_structure(self,table):
        sql = "PRAGMA table_info({})".format(table)
        if self.show_sql:
            print('执行sql:[{}]'.format(sql))
        for info in self.cu.execute(sql):
            print(info)
        self.conn.commit()
        self.close_all()



    def save(self, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                for d in data:
                    if self.show_sql:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    self.cu.execute(sql, d)
                self.conn.commit()
        else:
            print('the [{}] is empty or equal None!'.format(sql))



    def fetchall(self, sql):
        if sql is not None and sql != '':
            if self.show_sql:
                print('执行sql:[{}]'.format(sql))
            self.cu.execute(sql)
            return self.cu.fetchall()
        else:
             print('the [{}] is empty or equal None!'.format(sql))



    def fetchone(self, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                #Do this instead
                d = (data,)
                if self.show_sql:
                    print('执行sql:[{}],参数:[{}]'.format(sql, data))
                self.cu.execute(sql, d)
                return self.cu.fetchall()

            else:
                print('the [{}] equal None!'.format(data))
        else:
            print('the [{}] is empty or equal None!'.format(sql))


    def update(self, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                for d in data:
                    if self.show_sql:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    self.cu.execute(sql, d)
                    self.conn.commit()
        else:
             print('the [{}] is empty or equal None!'.format(sql))


    def delete(self, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                for d in data:
                    if self.show_sql:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    self.cu.execute(sql, d)
                    self.conn.commit()
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def pop_push(self,table):
        '''该方法为队列应用，从表中获取第一
           条数据，并删除，再将其放入表中最
           后一条，使其做到循环采集的功能'''
        if table is not None and table != '':

            sql = "SELECT * FROM {} limit 0,1".format(table)
            for info in self.cu.execute(sql):
                self.one_info = info
            delete_sql = "DELETE FROM {0} WHERE  ID = '{1}' ".format(str(table),str(self.one_info[0]))
            self.cu.execute(delete_sql)
            save_sql = '''INSERT INTO web_info values (?, ?, ?, ?, ?, ?)'''
            data = [('{}'.format(info[0]), '{}'.format(info[1]), '{}'.format(info[2]), '{}'.format(info[3]), info[4], info[5])]
            self.save(save_sql,data)
            self.conn.commit()
        else:
            print('the [{}] is empty or equal None!'.format(table))

    def info_map(self,name,data):
        create_table_sql = '''CREATE TABLE `{}`(`id` varchar(36) NOT NULL,`web_url` varchar(200) DEFAULT NULL,PRIMARY KEY (`id`))'''.format(name)
        self.create_table(create_table_sql)
        save_sql = '''INSERT INTO {} values (?, ?)'''.format(name)
        datas = list(map(lambda info:('{}'.format(uuid.uuid1()), '{}'.format(info)),data))
        self.save(save_sql,datas)

        pass
    def close_all(self):
         '''关闭数据库游标对象和数据库连接对象'''
         try:
             if self.cu is not None:
                 self.cu.close()
         finally:
             if self.cu is not None:
                 self.cu.close()

if __name__ =="__main__":

    sqlite = SqliteClient()

    ###########################################################################
    #'''删除数据库表'''
    # sqlite.drop_table("start_url")

    ###########################################################################
    # '''创建数据库表'''
    #
    # sql = '''CREATE TABLE `companys_info` (
    #                                                              `id` varchar(36) NOT NULL,
    #                                                              `company_name` varchar(50) NOT NULL,
    #                                                              `stock_code` varchar(200) DEFAULT NULL,
    #                                                               PRIMARY KEY (`id`)
    #                                                            )'''
    # sqlite.create_table(sql)
    #########################################################################
    # '''添加数据'''
    # save_sql = '''INSERT INTO companys_info values (?, ?, ?)'''
    # import uuid
    # data = [('{}'.format(uuid.uuid1()), '平安银行', '0000001'),
    #         ('{}'.format(uuid.uuid1()), '万科a', '000002',)]
    # sqlite.save(save_sql,data)

    #########################################################################
    # '''查询数据'''

    fetchall_sql = '''SELECT * FROM companys_info'''
    for info in sqlite.fetchall(fetchall_sql):
        print(info)

    # fetchone_sql = 'SELECT * FROM student WHERE ID = ? '
    # data = 1
    # for info in sqlite.fetchone(fetchone_sql,data):
    #     print(info)

    #########################################################################
    #更新数据
    # update_sql = 'UPDATE student SET name = HongtenAA WHERE ID = 1 '
    # data = [('HongtenAA', 1),
    #         ('HongtenBB', 2),
    #         ('HongtenCC', 3),
    #         ('HongtenDD', 4)]
    # sqlite.update(update_sql,data)

    #########################################################################
    #删除数据
    # delete_sql = 'DELETE FROM student WHERE NAME = ? AND ID = ? '
    # data = [('HongtenAA', 1),
    #         ('HongtenCC', 3)]
    # sqlite.delete(delete_sql,data)

    #########################################################################
    #构建数据集合
    # data = ["11111","22222","33333"]
    # sqlite.info_map(name="start_url",data=data)
    #获取表信息
    # sqlite.fetchall_table()
    #获取表机构
    # sqlite.table_structure("start_url")
    #删除第一条数据并将其添加到最后一行
    # sqlite.pop_push("web_info")
    # print(sqlite.one_info)
    #########################################################################


