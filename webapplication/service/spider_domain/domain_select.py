import pymysql


class domain_Select:
    def __init__(self):
        self.db = pymysql.connect(host='101.132.113.50', user='root', password='BlueSnail123!', db='spider_manage',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

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
            sort = int(data['sort'])
        except Exception as e:
            sort = 0

        try:
            status = int(data['status'])
        except Exception as e:
                status = 0

            # sql = "select * from main_url where webSite LIKE '%{}%'limit {}, {};".format(keyword, (page - 1) * limit,
            #                                                                              limit)
            # count_sql = "select count(*) from main_url where webSite LIKE '%{}%';".format(keyword)
        sql = "select * from main_url where status = {} and sort = {} and webSite LIKE '%{}%'limit {}, {};".format(status,sort, keyword,
                                                                                                   (page - 1) * limit,
                                                                                                   limit)
        count_sql = "select count(*) from main_url where status = {} and sort = {} and webSite LIKE '%{}%';".format(status,sort, keyword)


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
    select = domain_Select()
    data = {'sort': '0', 'page': '1', 'limit': '10','status':0}
    for item in select.select_all(data).get("data"):
        print(item)