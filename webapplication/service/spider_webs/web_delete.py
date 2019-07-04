import pymysql


class WebDelete:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def delete_one(self, data):
        id = data['id']
        sql = 'delete from webinfo where id="%s"' % id
        cursors = self.db.cursor()
        try:
            cursors.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.db.close()
