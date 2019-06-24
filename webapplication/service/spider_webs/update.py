import pymysql


class Update:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def update(self, data):
        id = data['id']
        remark = data['remark']
        sql = 'update webinfo set remark="%s" where id="%s"' % (remark, id)
        cursors = self.db.cursor()
        try:
            cursors.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.db.close()

    def update_status(self, data):
        id = data['id']
        try:
            status = int(data['status'])
            sql = 'update webinfo set status=%d where id="%s"' % (status, id)
        except:
            pass
        try:
            checked = int(data['checked'])
            sql = 'update webinfo set checked=%d where id="%s"' % (checked, id)

        except:
            pass


        cursors = self.db.cursor()
        try:
            cursors.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.db.close()
