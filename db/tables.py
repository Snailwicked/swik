# -*-coding:utf-8 -*-
from sqlalchemy import Table, Column, INTEGER, String,DATE,TEXT,JSON,DateTime
from db.basic import metadata
import uuid

def index_uuid():
   return uuid.uuid4().hex




main_url = Table("main_url", metadata,
                Column("pid", INTEGER, primary_key=True, autoincrement=True),
                Column("address", String(500), default='', server_default=''),
                Column("webSite", String(500), default='', server_default=''),
                Column("sort", INTEGER, default=101, server_default='101'),
                Column("status", INTEGER, default=0, server_default='0'),
                Column("remark", String(200), default='', server_default=''),
                Column("spider_name", INTEGER, default=0, server_default='0'),
                Column("rule", JSON)

)


spider_task = Table("spider_task", metadata,
                Column("id", INTEGER, primary_key=True, autoincrement=True),
                Column("task_name", String(500), default='', server_default=''),
                Column("create_time", DATE ,nullable=False),
                Column("status", INTEGER, default=0, server_default='0'),
                Column("creater", String(500), default="", server_default=''),
                Column("config", String(500), default="", server_default=''),
                )


__all__ = ['main_url','spider_task']