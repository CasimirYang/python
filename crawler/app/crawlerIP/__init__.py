#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class IpInfo(object):
    __slots__ = ('ip', 'host', 'user', 'password', 'type', 'location') # 用tuple定义允许绑定的属性名称

    def __init__(self, ip, host, user='', password='', type='http', location='CN'):
        self.ip = ip
        self.host = host
        self.user = user
        self.password = password
        self.type = type
        self.location = location  #todo @property


