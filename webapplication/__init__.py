import requests
response = requests.get("http://e.weibo.com/n1/2019/0829/c40606-31323795.html")
print(response.status_code)