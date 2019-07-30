from db import main_url
from db import web_info


'''
32.75

'''
if __name__ == '__main__':
    parameter = {
        "page": 1,
        "limit": 10,
        "status": 1,
        "sort": 0,
        "keyword": "法制周末"
    }

    for item in main_url.select_main_url(parameter)["data"]:
        print("=======================分界线=======================")
        parameters = {
            "page": 1,
            "limit": 10,
            "status": 0,
            "checked": 0,
            "pid": item["pid"]
        }
        infos = web_info.select_web_info(parameters)
        print(item["address"]+"   网站有 {} 个子页".format(str(infos['count'])))
        for data in infos['data']:
            print(data)
