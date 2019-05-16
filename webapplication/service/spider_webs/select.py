import pymysql


class Select:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def select_all(self, data):
        """
        启用网址
        :return: data
        """
        page = int(data['page'])
        limit = int(data['limit'])
        sql = "select * from webinfo where status=%d order by add_time desc limit %d, %d" % (1, (page-1)*limit, limit)
        count_sql = 'select * from webinfo where status=%d' % 1
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

    def select_off(self, data):
        """
        停用网址
        :return: data
        """
        page = int(data['page'])
        limit = int(data['limit'])
        sql = "select * from webinfo where status=%d order by add_time desc limit %d, %d" % (0, (page-1)*limit, limit)
        count_sql = 'select * from webinfo where status=%d' % 0
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


if __name__ == "__main__":
    select = Select()
    select.select_off({'page': 1, 'limit': 10})
