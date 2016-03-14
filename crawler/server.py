#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import tornado
from tornado.options import define, options
from tornado.web import RequestHandler
import tornado.httpserver
import url
from app.crawlerIP.schudulerJob import schudulerStart

define("port", default=8000, help="run on the given port", type=int)


setting = dict(
  template_path=os.path.join(os.path.dirname(__file__), "templates"),
  static_path=os.path.join(os.path.dirname(__file__), "static"),
  )

handlers = []
##根据web.ini设定相关参数
def application_setting_handle():
    # _config=WebConfig() todo: get from config file
    # setting["template_path"]=_config.cf.get("web", "template_path")
    # setting["static_path"]=_config.cf.get("web", "static_path")
    #--这里要加入静态文件的直接访问。
    handlers.append((r"/data/(.*)", tornado.web.StaticFileHandler, {"path": "data"}))     #这是data静态文件，用自定义静态文件的路由。
    handlers.append((r"/images/(.*)", tornado.web.StaticFileHandler, {"path": "images"})) #这是images静态文件，用自定义静态文件的路由。
    handlers.append((r"/upload/(.*)", tornado.web.StaticFileHandler, {"path": "upload"})) #这是上传的静态文件，用自定义静态文件的路由。
    handlers.extend(url.url) #pc端页面。

if __name__ == "__main__":
    #schudulerStart()
    # conf_server=ServerConfig() #读取server的配置文件。
    # options.port=int(conf_server.getPort())
    tornado.options.parse_command_line()
    application_setting_handle()
    app = tornado.web.Application(handlers=handlers, **setting)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()