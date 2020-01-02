import pymysql
class DbToMysql(object):

    def __init__(self):
        self.con = pymysql.connect(
            host="180.97.15.173",
            user="wzh",
            password="wzh234287",
            db="bgnet",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        self.con.close()

    def save_one_data(self,datas):
        sql = "INSERT INTO `bgnet_intelligence` (person_id,collector_id,user_id,title,translat_title,hand_translat_title,type_way,type,translat_type,hand_translat_type,original_link,translat_original_link,hand_translat_original_link,web_site,translat_web_site,hand_translat_web_site,country,translat_country,hand_translat_country,content,translat_content,hand_translat_content,status,create_time,update_time,is_del,longitude,latitude,remark,mark) " \
              "VALUES ('0', NULL, NULL,'{0}' ,'{1}', NULL, 0, 0, NULL, NULL,'{2}', NULL, NULL, '{3}', NULL, NULL, '{4}', NULL, NULL, '{5}', '{6}', NULL, 0, '{7}', NULL, 0, '{8}', '{9}', NULL, NULL)".format(str(datas['title']),str(datas['translat_title']),datas['original_link'],datas['web_site'],datas['country'],str(datas['content']),str(datas['translat_content']),datas['create_time'],datas['longitude'],datas['latitude'])
        try:
            with self.con.cursor() as cursor:
                print(cursor.execute(sql))
                self.con.commit()
        except Exception as e:
            return -1
        # finally:
        #     self.close()

    def select_by_page(self,page):
        sql = 'select * from bgnet_intelligence limit {},1000'.format((page-1)*1000)
        print(sql)
        try:
            with self.con.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                self.con.commit()
                return result
        except Exception as e:
            return [e]

    def delete_by_id(self,id):
        sql = 'DELETE from bgnet_intelligence  WHERE id = {};'.format(int(id))
        print(sql)
        try:
            with self.con.cursor() as cursor:
                cursor.execute(sql)
                self.con.commit()
        except Exception as e:
            return [e]

dbsql = DbToMysql()
# from utils.base_utils.bloomfilter import filter
# for page in range(1,13):
#     filter_title = filter("./news.blm")
#     for item in dbsql.select_by_page(page):
#         result = filter_title.filter_text(item.get("title"))
#         if not result:
#             dbsql.delete_by_id(item.get("id"))
#     filter_title.tofile()
