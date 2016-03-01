#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

import itertools
import requests
from bs4 import BeautifulSoup

from crawlerIP.connectTest import connectTest
from crawlerIP.dbUtil import saveToNeo

class ipInfo(object):
    __slots__ = ('ip', 'host', 'user', 'password','type','location') # 用tuple定义允许绑定的属性名称

    def __init__(self, ip, host, user='', password='',type='http',location='CN'):
        self.ip = ip
        self.host = host
        self.user = user
        self.password = password
        self.type = type
        self.location =location

def proxy360():
    ipInfoList = []
    url = 'http://www.proxy360.cn/Proxy'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for item in soup.select(".proxylistitem"):
        ipHost = item.find("div").find_all("span", limit=2)
        ip = str(ipHost[0].string).strip()
        host = str(ipHost[1].string).strip()
        ipInfoList.append(ipInfo(ip, host))
        #print(ipInfoList) #todo
        return ipInfoList

# ipInfoList = connectTest(proxy360())
# print(len(ipInfoList))
# if(len(ipInfoList)>0):
#     saveToNeo(ipInfoList)

def xicidaili(urlList):
    for url in urlList:
        natuals = itertools.count(1)
        ns = itertools.takewhile(lambda x: x <= 10, natuals)
        for i in list(ns):
            url= url+str(i)
            ipInfoList = connectTest(xicidailiSinglePage(url))
            print(len(ipInfoList))
            if(len(ipInfoList)>0):
                saveToNeo(ipInfoList)

def xicidailiSinglePage(url):
    ipInfoList = []
    #url = 'http://www.xicidaili.com/'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    for item in soup.select(".odd"):
        ipHost = item.find_all("td")
        ip = str(ipHost[2].string).strip()
        host = str(ipHost[3].string).strip()
        type = str(ipHost[6].string).strip()
        ipInfoList.append(ipInfo(ip, host,type=type))
        print("{0}:{1} {2}".format(ip,host,type))
    return ipInfoList

# urlList=[]
# urlList.append("http://www.xicidaili.com/nn/")
# urlList.append("http://www.xicidaili.com/nt/")
# urlList.append("http://www.xicidaili.com/wn/")
# urlList.append("http://www.xicidaili.com/wt/")
# xicidaili(urlList)


#http://ip.zdaye.com/dayProxy/2016/3/1.html



# url = 'http://apis.baidu.com/apistore/iplookupservice/iplookup?ip=46.61.143.178'
# headers= {"apikey":"98b0fd667b061d25c9aea82c0f42d0b5"}
# response = requests.get(url,headers=headers)
# print(response.content)
# print(response.json())
# url="http://www.google.com"
# proxies ={'http':"http://46.61.143.178:8080"}
# response = requests.get(url)
# print(response.text)
# print(response.status_code)

