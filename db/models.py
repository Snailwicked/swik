# -*-coding:utf-8 -*-
from db.basic import Base
from db.tables import *
import json


class MainUrl(Base):
    __table__ = main_url

    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class WebInfo(Base):
    __table__ = webinfo
    def json(self):
        return {"id":self.id,"url":self.url,"info":self.info,"add_time":self.add_time,"agent":self.agent,"status":self.status,
                    "web_name": self.web_name, "sort": self.sort, "total": self.total, "checked": self.checked,"is_starting": self.is_starting, "remark": self.remark,
                         "spider_name": self.spider_name, "pid": self.pid}