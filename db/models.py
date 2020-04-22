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


class User(Base):
    __table__ = user

    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class KeyWords(Base):
    __table__ = key_words

    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class WordList(Base):
    __table__ = word_list

    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}