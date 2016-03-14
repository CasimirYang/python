#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tornado

from app.zhihu.dbUtil import get_total_user, get_total_relationshiop


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class GetTotalUser(tornado.web.RequestHandler):
     def post(self):
        print("哈哈 我进来了~~~GetTotalUser")
        total_user = get_total_user()
        self.write(total_user)


class GetTotalRelationship(tornado.web.RequestHandler):
     def post(self):
        print("哈哈 我进来了~~~GetTotalRelationship")
        total_relationshiop = get_total_relationshiop()
        self.write(total_relationshiop)


class ReflushIP(tornado.web.RequestHandler):
     def get(self):
        print("哈哈 我进来了~~~ReflushIP")
        self.render('index2.html')
