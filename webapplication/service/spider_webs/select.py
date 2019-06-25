import pymysql


class Select:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    # def select_all(self, data):
    #     """
    #     启用网址
    #     :return: data
    #     """
    #     page = int(data['page'])
    #     limit = int(data['limit'])
    #     sql = "select * from webinfo where status=%d order by add_time desc limit %d, %d" % (1, (page-1)*limit, limit)
    #     count_sql = 'select * from webinfo where status=%d' % 1
    #     cursors = self.db.cursor()
    #     try:
    #         cursors.execute(sql)
    #         data = cursors.fetchall()
    #         count = cursors.execute(count_sql)
    #         data = {'data': data, 'count': count}
    #         self.db.commit()
    #         return data
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         self.db.close()
    #
    # def select_off(self, data):
    #     """
    #     停用网址
    #     :return: data
    #     """
    #     page = int(data['page'])
    #     limit = int(data['limit'])
    #     sql = "select * from webinfo where status=%d order by add_time desc limit %d, %d" % (0, (page-1)*limit, limit)
    #     count_sql = 'select * from webinfo where status=%d' % 0
    #     cursors = self.db.cursor()
    #     try:
    #         cursors.execute(sql)
    #         data = cursors.fetchall()
    #         count = cursors.execute(count_sql)
    #         data = {'data': data, 'count': count}
    #         self.db.commit()
    #         return data
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         self.db.close()

    def select_all(self, data):
        """
        通过status参数展示正在采集和待采集
        :param data:
        :return:
        """
        try:
            page = int(data['page'])
            limit = int(data['limit'])
        except Exception as e:
            print(e)

        try:
            keyword = str(data['keyword'])
        except Exception as e:
            keyword = ""

        try:
            status = int(data['status'])
        except Exception as e:
            status = 1
        try:
            checked = str(data['checked'])
        except Exception as e:
            checked = 1
        try:
            is_starting = str(data['is_starting'])
            sql = "select * from webinfo where status = {} and checked={} and is_starting = {} and web_name LIKE '%{}%'limit {}, {};".format(
                status, checked, is_starting, keyword, (page - 1) * limit, limit)
            count_sql = "select count(*) from webinfo where status = {} and checked={} and is_starting = {}  and web_name LIKE '%{}%';".format(
                status, checked, is_starting, keyword)
        except Exception as e:
            sql = "select * from webinfo where status = {} and checked={} and web_name LIKE '%{}%'limit {}, {};".format(
                status, checked, keyword, (page - 1) * limit, limit)
            count_sql = "select count(*) from webinfo where status = {} and checked={}  and web_name LIKE '%{}%';".format(
                status, checked, keyword)


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
    data = {'is_starting': '1', 'page': '1', 'limit': '10', 'status': '1', 'checked': '1'}
    for item in select.select_all(data).get("data"):
        print(item)