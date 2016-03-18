#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import tornado

from app.crawlerIP.ipCrawler import ip_crawler
from app.zhihu.dbUtil import get_total_user, get_total_relationshiop

logger = logging.getLogger("tornado.access")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ReflushIP(tornado.web.RequestHandler):
     def post(self):
        logger.info("begin to reflush ip")
       # ip_crawler()
        self.write("Done !")


class StopZhihu(tornado.web.RequestHandler):
    def post(self):
#todo
        self.write("")


class GetTotalUser(tornado.web.RequestHandler):
     def post(self):
        print("哈哈 我进来了~~~GetTotalUser")
        total_user = get_total_user()
        self.write(str(total_user))


class GetTotalRelationship(tornado.web.RequestHandler):
     def post(self):
        print("哈哈 我进来了~~~GetTotalRelationship")
        total_relationshiop = get_total_relationshiop()
        self.write(str(total_relationshiop))
