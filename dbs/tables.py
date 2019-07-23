# -*-coding:utf-8 -*-
from sqlalchemy import Table, Column, INTEGER, String,DATE
from dbs.basic_db import metadata


main_url = Table("main_url", metadata,
                Column("pid", INTEGER, primary_key=True, autoincrement=True),
                Column("address", String(500), default='', server_default=''),
                Column("webSite", String(500), default='', server_default=''),
                Column("sort", INTEGER, default=101, server_default='101'),
                Column("status", INTEGER, default=0, server_default='0'),
                Column("remark", String(200), default='', server_default='')
            )


webinfo = Table("webinfo", metadata,
                Column("id", String(500), primary_key=True),
                Column("url", String(500), default='', server_default=''),
                Column("info", String(500), default='', server_default=''),
                Column("add_time", DATE, default="", server_default=''),
                Column("agent", INTEGER, default=0, server_default='0'),
                Column("status", INTEGER, default=0, server_default='0'),
                Column("web_name", String(500), default="", server_default=''),
                Column("sort", INTEGER, default=0, server_default='0'),
                Column("total", INTEGER, default=0, server_default='0'),
                Column("checked", INTEGER, default=0, server_default='0'),
                Column("is_starting", INTEGER, default=0, server_default='0'),
                Column("remark", String(500), default="", server_default=''),
                Column("spider_name", String(500), default="", server_default=''),
                Column("pid", INTEGER, default=0, server_default='0')

                )


__all__ = ['main_url','webinfo']