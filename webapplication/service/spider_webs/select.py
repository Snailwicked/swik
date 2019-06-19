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
        全部先展示status=1
        :param data:
        :return:
        """
        try:
            page = int(data['page'])
            limit = int(data['limit'])
        except:
            pass
        try:
            status = int(data['status'])
        except:
            status = 1
        try:
            keyword = str(data['keyword'])
        except:
            keyword = ""

        sql = "select * from webinfo where status = {} and web_name LIKE '%{}%'limit {}, {};" .format(status,keyword,(page-1)*limit, limit)
        count_sql = "select count(*) from webinfo where status = {} and web_name LIKE '%{}%';" .format(status,keyword)
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


if __name__ == "__main__":
    select = Select()
    result = select.select_all({'status': '0', 'page': '3', 'limit': '10'})
    print(result)
