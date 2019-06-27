import pymysql


class Select:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


    def select_all(self, data):
        """
        通过status参数展示正在采集和待采集
        :param data:
        :return:
        """
        page = int(data['page'])
        limit = int(data['limit'])
        pid = str(data['pid'])
        if len(data)==3:
            try:
                sql = "select * from webinfo where pid = {} limit {}, {};".format(pid,(page - 1) * limit, limit)
                count_sql = "select count(*) from webinfo where pid = {}".format(pid)
            except Exception as e:
                print(e)
        else:
            try:
                status = int(data['status'])
            except Exception:
                pass
            try:
                checked = str(data['checked'])
            except Exception:
                pass
            sql = "select * from webinfo where pid = {} and  status = {} and checked={} limit {}, {};".format(pid,
                    status, checked, (page - 1) * limit, limit)
            count_sql = "select count(*) from webinfo where pid = {} and  status = {} and checked={}".format(pid,
                    status, checked)

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
    select = Select()
    data = {'pid': 6104, 'page': '1', 'limit': '10', 'status': '1', 'checked': '1'}
    for item in select.select_all(data).get("data"):
        print(item)