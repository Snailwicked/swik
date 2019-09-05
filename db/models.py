# -*-coding:utf-8 -*-
from db.basic import Base
from db.tables import *
import json


class MainUrl(Base):
    __table__ = main_url

    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class SpiderTask(Base):
    __table__ = spider_task

    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
