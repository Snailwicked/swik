# coding: utf-8

import xlrd
from xlrd import xldate_as_tuple
import multiprocessing
import json
import os
import datetime
import traceback


class ExcelToJson:

    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_brief(self, info):
        out = info[0]
        keys = str(info[1])
        if ':' in keys:
            keys = keys.split(':')
        return out, keys

    def filter_invalid_rows(self, sheet, rows=None):
        rows = rows or 1
        rowe = sheet.nrows
        while rows < rowe:
            fields = sheet.row_values(rows)
            if '#' in str(fields):
                rows = rows + 1
                continue
            else:
                break
        return rows

    def check_keys_col(self, rowdict, keys):
        if isinstance(keys, list):
            for key in keys:
                if not rowdict[key] or rowdict[key] == '':
                    return False
        else:
            if not rowdict[keys] or rowdict[keys] == '':
                return False
        return True

    # 关联表的id检查
    def get_data_rows(self, excelName):
        excelFile = xlrd.open_workbook(excelName)
        excelSheetNames = excelFile.sheet_names()
        sheet = excelFile.sheet_by_name(excelSheetNames[0])
        info = sheet.row_values(0)
        if info is None:
            return False
        rowe = sheet.nrows
        if rowe == 1:
            return False
        rows = self.filter_invalid_rows(sheet)
        if rows <= 1:
            return False
        rows = rows + 1
        if rows == rowe:
            return False
        rows = self.filter_invalid_rows(sheet, rows)
        return True, rows, rowe, sheet

    def check_union_keys(self, tb1, tb2):
        ret, rows1, rowe1, sheet1 = self.get_data_rows(tb1)
        if not ret:
            return False
        ret, rows2, rowe2, sheet2 = self.get_data_rows(tb2)
        if not ret:
            return False
        keylist1 = sheet1.col_values(1)[rows1:rowe1]
        for i in range(0, len(keylist1)):
            if not isinstance(keylist1[i], str):
                keylist1[i] = str(keylist1[i])
        keylist1.sort()
        keylist2 = sheet2.col_values(0)[rows1:rowe1]
        for i in range(0, len(keylist2)):
            if not isinstance(keylist2[i], str):
                keylist2[i] = str(keylist2[i])
        keylist2.sort()
        if len(keylist1) == len(keylist2):
            for i in range(0, len(keylist1)):
                if keylist1[i] == keylist2[i]:
                    continue
                else:
                    return False
        else:
            return False
        return True

    def fix_rowdict(self, attr, rowdict):
        for key in rowdict:
            colv = rowdict[key]
            if attr[key] == "int" or attr[key] == "float":
                if colv == '':
                    colv = 0
            if attr[key] == "int":
                colv = int(colv)
            if attr[key] == "float":
                colv = float(colv)
            if attr[key] == "bool":
                colv = bool(colv)
            if attr[key] == "string":
                if isinstance(colv, float):
                    colv = int(colv)
                colv = str(colv)
            if attr[key] == "date":
                if colv == '' or colv == None:
                    raise Exception("日期不能为空")
                dt = xldate_as_tuple(colv, 0)
                dt = datetime.datetime(*dt)
                colv = str(dt)
            rowdict[key] = colv
        return rowdict

    def get_jsonkey(self, rowdict, keys):
        if isinstance(keys, list):
            keyv = []
            for key in keys:
                if rowdict[key] is None:
                    raise ("error")
                else:
                    keyv.append(str(rowdict[key]))
            if keyv:
                return '_'.join(keyv)
        else:
            if rowdict[keys] is None:
                raise ("error")
            return str(rowdict[keys])

    def read_excel(self, excelName, outpath):
        fields = []
        datatypes = []
        attr = dict()
        colsLen = 0
        try:
            excelFile = xlrd.open_workbook(excelName)
            excelSheetNames = excelFile.sheet_names()
            # print(excelSheetNames)
            sheet = excelFile.sheet_by_name(excelSheetNames[0])
            # print(sheet.name,sheet.nrows,sheet.ncols)
            info = sheet.row_values(0)
            if info is None:
                raise ('请给出表简要信息')
            colsLen = info.index('#')
            out, keys = self.get_brief(info[:colsLen])
            outfile = outpath + out + ".json"
            rowe = sheet.nrows
            if rowe == 1:
                raise ("表错误")
            rows = self.filter_invalid_rows(sheet)
            if rows <= 1:
                raise ("表错误")
            tempfields = sheet.row_values(rows)[:colsLen]
            for temp in tempfields:
                l = temp.split(":")
                fields.append(l[0].strip().lower())
                datatypes.append(l[1].strip().lower())
            attr = dict(zip(fields, datatypes))
            rows = rows + 1
            if rows == rowe:
                raise ("表错误")
            rows = self.filter_invalid_rows(sheet, rows)
            allrows = dict()
            while rows < rowe:
                rowv = sheet.row_values(rows)[:colsLen]
                rows = rows + 1
                if '#' in str(rowv[0]):
                    continue
                rowdict = dict(zip(fields, rowv))
                if not self.check_keys_col(rowdict, keys):
                    raise ("keys error")
                rowdict = self.fix_rowdict(attr, rowdict)
                jsonkey = self.get_jsonkey(rowdict, keys)
                allrows[jsonkey] = rowdict
            # 写入文件
            with open(outfile, 'w+') as f:
                jsonStr = json.dumps(
                    allrows, indent=4, sort_keys=False, ensure_ascii=False)
                f.write(jsonStr + '\n')

        except Exception as e:
            print('str(Exception):\t', str(e))
            print('traceback.print_exc():', traceback.print_exc())

    def get_excels(self, srcDir):
        files = os.listdir(srcDir)
        excels = [file for file in files if os.path.splitext(
            file)[1] == '.xlsx' and '~' not in file]
        return excels


if __name__ == '__main__':
    srcDir = "Y:\\testcpp\\"
    desDir = "Y:\\testcpp\\"
    excelToJson = ExcelToJson()
    ret = excelToJson.check_union_keys("Y:\\testcpp\\test1.xlsx",
                                       "Y:\\testcpp\\test2.xlsx")
    if not ret:
        print('Foreign key error')
        os._exit()

    excels = excelToJson.get_excels(srcDir)
    pool = multiprocessing.Pool(processes=5)
    for excel in excels:
        srcFile = srcDir + excel
        # read_excel(srcFile, desDir)
        pool.apply_async(excelToJson.read_excel, (srcFile, desDir))
    pool.close()
    pool.join()