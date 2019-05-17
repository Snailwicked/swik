import pymysql


class TaskSelect:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def select_off(self, data):
        page = int(data['page'])
        limit = int(data['limit'])
        sql = "select * from spider_task where status=%d order by create_time desc limit %d, %d" % (0, (page-1)*limit,
                                                                                                    limit)
        count_sql = "select * from spider_task where status=%d" % 0
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

