# from flask_pymongo import PyMongo
# from flask import Flask
#
#
# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://101.132.113.50:27017/spider_manage"
# mongo = PyMongo(app)
# resp = mongo.db.config.find_one_or_404({'uuid': '97a4b480-67ec-11e9-b9d6-9c5c8ed1c019'})['fixed_time']
# print(resp)
x = [ [1,3,3],[2,3,1]]
y = sorted(x,key = lambda item:(item[0],-item[2]))
print(y)