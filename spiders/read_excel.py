import xlrd
import time


'''
数据库插入类
'''
from dateutil.parser import parse as date_parser

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
        print(sql)
        try:
            with self.con.cursor() as cursor:
                result = cursor.execute(sql)
                self.con.commit()
                return result
        except Exception as e:
            return -1
        # finally:
        #     self.close()

dbsql = DbToMysql()


'''
读取excel
'''

file = 'excel_data29.xls'
def read_excel():
    count = 0
    data = {}
    wb = xlrd.open_workbook(filename=file)#打开文件
    sheet1 = wb.sheet_by_index(0)
    rows_num = sheet1.nrows
    print(rows_num)
    for i in range(2,rows_num):
        data["title"] = str(sheet1.cell_value(i, 0)).replace("'","").replace("\n","")
        data["translat_title"] = sheet1.cell_value(i, 1).replace("'","").replace("\n","")
        data["country"] = sheet1.cell_value(i, 2).replace("'","").replace("\n","")
        data["original_link"] = sheet1.cell_value(i, 3).replace("'","").replace("\n","")
        data["web_site"] = sheet1.cell_value(i, 4).replace("'","").replace("\n","")
        data["longitude"] =95.712891
        data["latitude"] = 37.090240
        data["content"] = sheet1.cell_value(i, 7).replace("'","").replace("\n","")
        data["translat_content"] = sheet1.cell_value(i, 8).replace("'","").replace("\n","")
        timeArray = time.localtime(
            int(time.mktime(date_parser(str(sheet1.cell_value(i, 9)).replace("\\n", "").replace("\\t", "")).timetuple())))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data["create_time"] = otherStyleTime
        print(data)
        result = dbsql.save_one_data(data)
        if result ==1:
            count = count+1
    print(count)
read_excel()
