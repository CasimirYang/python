#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app.controller import IndexHandler, ReflushIP, StopZhihu, GetTotalRelationship, GetTotalUser

url = [
    #(r"/data/(.*)", tornado.web.StaticFileHandler,{"path":"data"})#这是data静态文件，用自定义静态文件的路由。
    (r"/", IndexHandler),
    (r"/stopZhihu", StopZhihu),
    (r"/reflushIP", ReflushIP),
    (r"/GetTotalUser", GetTotalUser),
    (r"/GetTotalRelationship", GetTotalRelationship)
]