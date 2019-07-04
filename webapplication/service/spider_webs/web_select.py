import pymysql


class WebSelect:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


    def select_all(self, data):
        """
        通过status参数展示正在采集和待采集
        :param data:
        :return:
        """
        print(data)
        status = str(data['status'])
        checked = str(data['checked'])
        page = int(data['page'])
        limit = int(data['limit'])
        pid = int(data['pid'])

        if status=="" or checked =="" or (status=="" and checked ==""):
            sql = "select * from webinfo where pid = {} limit {}, {};".format(pid, (page - 1) * limit, limit)
            count_sql = "select count(*) from webinfo where pid = {}".format(pid)
        else:
            sql = "select * from webinfo where pid = {} and  status = {} and checked={} limit {}, {};".format(pid,
                    int(status), int(checked), (page - 1) * limit, limit)
            count_sql = "select count(*) from webinfo where pid = {} and  status = {} and checked={}".format(pid,
                    int(status), int(checked))
        cursors = self.db.cursor()
        try:
            cursors.execute(sql)
            data = cursors.fetchall()
            cursors.execute(count_sql)
            count = list(cursors.fetchone().values())[0]
            data = {'data': data, 'count': count}
            self.db.commit()
            return data
        except Exception as e:
            print(e)
        finally:
            self.db.close()

if __name__ == '__main__':
    select = WebSelect()
    data = {'pid': 6104, 'page': '1', 'limit': '10', 'status': '1', 'checked': '1'}
    for item in select.select_all(data).get("data"):
        print(item)