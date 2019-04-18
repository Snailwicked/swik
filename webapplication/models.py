from .ext import db
from flask_login import UserMixin
import datetime
import hashlib


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

    def __init__(self, url, web_name, status, agent, sort):
        hl = hashlib.md5()
        self.url = url
        hl.update(url.encode("utf8"))
        self.id = hl.hexdigest()
        self.add_time = datetime.datetime.now()
        self.web_name = web_name
        self.status = status
        self.agent = agent
        self.sort = sort


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
