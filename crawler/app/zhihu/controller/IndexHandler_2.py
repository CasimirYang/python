#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tornado.web import RequestHandler


class IndexHandler_2(RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user_2!')