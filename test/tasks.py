import xlrd

file = 'excel.xls'

def read_excel():
    data = {}
    wb = xlrd.open_workbook(filename=file)#打开文件
    sheet1 = wb.sheet_by_index(0)
    for i in range(2,128):
        data["title"] = sheet1.cell_value(i, 0)
        data["translat_title"] = sheet1.cell_value(i, 1)
        data["country"] = "美国"
        data["original_link"] = sheet1.cell_value(i, 3)
        data["web_site"] = sheet1.cell_value(i, 4)
        data["longitude"] =95.712891
        data["latitude"] = 37.090240
        data["content"] = sheet1.cell_value(i, 7)
        data["translat_content"] = sheet1.cell_value(i, 8)
        data["translat_content"] = "2019-09-27"

        print(data)
read_excel()