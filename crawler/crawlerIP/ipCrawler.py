#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

from crawlerIP.dbUtil import saveToNeo


class ipInfo(object):
    __slots__ = ('ip', 'host', 'user', 'password') # 用tuple定义允许绑定的属性名称

    def __init__(self, ip, host, user='', password=''):
        self.ip = ip
        self.host = host
        self.user = user
        self.password = password



ipInfoList = []
url = 'http://www.proxy360.cn/Proxy'
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
for item in soup.select(".proxylistitem"):
    ipHost = item.find("div").find_all("span", limit=2)
    ip = str(ipHost[0].string).strip()
    host = str(ipHost[1].string).strip()
    ipInfoList.append(ipInfo(ip, host))
print(ipInfoList) #todo

#todotest connect

saveToNeo(ipInfoList)
