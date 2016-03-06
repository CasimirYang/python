#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app.zhihu.controller import IndexHandler
from app.zhihu.controller.IndexHandler_2 import IndexHandler_2

url=[
    #(r"/data/(.*)", tornado.web.StaticFileHandler,{"path":"data"})#这是data静态文件，用自定义静态文件的路由。
    (r"/test", IndexHandler)
    #pc版页面，
    ,(r"/index\.html", IndexHandler_2)
    ]