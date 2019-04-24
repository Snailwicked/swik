from .ext import db
from flask_login import UserMixin
import datetime
import hashlib
import uuid
from flask_login import current_user


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
    total = db.Column(db.Integer, nullable=True)  # 采集总量，明辉mongodb的爬虫配置信息会存进来，读就完事

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


class SpiderTask(db.Model):
    __tablename__ = "spider_task"
    id = db.Column(db.String(100), primary_key=True)  # uuid md5加密
    task_name = db.Column(db.String(255), nullable=False)
    task_job = db.Column(db.Binary(255), nullable=False)  # 二进制文件
    create_time = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)  # 0未启动 1启动
    creater = db.Column(db.String(255), nullable=False)
    config_name = db.Column(db.String(255), nullable=True)  # 用于查询mongodb的配置表信息
    result_name = db.Column(db.String(255), nullable=True)  # 用于查询mongodb存储的结果信息

    def __init__(self, task_name, task_job, status, config_name, result_name):
        self.id = uuid.uuid3()
        self.task_name = task_name
        self.task_job = task_job
        self.status = status
        self.config_name = config_name
        self.result_name = result_name
        self.create_time = datetime.datetime.now()
        self.creater = current_user.username




