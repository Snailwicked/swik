import pymysql


class DomainUpdate:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


    def execute(self,sql):
        cursors = self.db.cursor()
        try:
            cursors.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)

    def update(self, data):
        id = data['pid']
        try:
            remark = data['remark']
            sql = 'update main_url set remark={} where pid={}'.format(remark, id)
        except:
            pass

        try:
            status = int(data['status'])
            sql = 'update main_url set status={} where pid={}'.format(status, id)
        except:
            pass

        self.execute(sql)


if __name__ == '__main__':
    select = DomainUpdate()
    data = {'pid': 5905, 'remark': '网站404'}
    select.update(data)
