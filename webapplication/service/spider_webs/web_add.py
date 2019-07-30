import datetime
import pymysql
import hashlib


class WebAdd:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def add_one(self, data):
        web_url = data['web_url']
        hl = hashlib.md5()
        hl.update(web_url.encode("utf8"))
        id = hl.hexdigest()
        add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        agent = int(data['agent'])
        status = 0
        web_name = data['web_name']
        sort = int(data['sort'])
        pid = int(data['pid'])
        cursors = self.db.cursor()
        try:
            sql = 'insert into webinfo(id, url, add_time, agent, status, web_name, sort) values ("%s", "%s", "%s", "%d", "%d", "%s", "%d")' % (id, web_url, add_time, agent, status, web_name, sort)
            cursors.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.db.close()
