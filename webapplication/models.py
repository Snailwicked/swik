from .ext import db
from flask_login import UserMixin
import datetime


class WebInfo(db.Model):
    __tablename__ = 'webinfo'
    id = db.Column(db.Integer, primary_key=True)  # url md5加密
    url = db.Column(db.String(1024), nullable=False)
    web_name = db.Column(db.String(1024), nullable=True)
    info = db.Column(db.String(1024), nullable=True)  # 备用的
    add_time = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Integer, nullable=True, default=0)  # 0说明没有采集  1被采集了
    agent = db.Column(db.Integer, nullable=True)  # 0国内  1国外
    sort = db.Column(db.Integer, nullable=True)  # 1 通用型 2 登录型 3 特殊型

    def __init__(self, url):
        self.url = url
        self.add_time = datetime.datetime.now()


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
