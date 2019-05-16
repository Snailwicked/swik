import pymysql


class Update:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def update(self, data):
        web_name = data['web_name']
        url = data['web_url']
        agent = int(data['agent'])
        sort = int(data['sort'])
        sql = 'update webinfo set web_name="%s", url="%s", agent=%d, sort=%d' % (web_name, url, agent, sort)
        cursors = self.db.cursor(sql)
        try:
            cursors.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.db.close()

    def update_status(self, data):
        id = data['id']
        status = int(data['status'])
        sql = 'update webinfo set status=%d where id="%s"' % (status, id)
        cursors = self.db.cursor()
        try:
            cursors.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
        finally:
            self.db.close()
