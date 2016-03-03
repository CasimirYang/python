#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
http://www.proxy360.cn/Proxy
http://www.xicidaili.com/
http://ip.zdaye.com/dayProxy/2016/3/1.html
https://www.imfreevpn.com/
"""

import itertools
import requests
from bs4 import BeautifulSoup

from crawlerIP import IpInfo


def proxy360():
    ipInfoList = []
    url = 'http://www.proxy360.cn/Proxy'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for item in soup.select(".proxylistitem"):
        ipHost = item.find("div").find_all("span", limit=2)
        ip = str(ipHost[0].string).strip()
        host = str(ipHost[1].string).strip()
        ipInfoList.append(IpInfo(ip, host))
        #print(IP_INFOList) #todo
    return ipInfoList


def xicidaili():
    ipInfoList = []
    urlList = []
    urlList.append("http://www.xicidaili.com/nn/")
    urlList.append("http://www.xicidaili.com/nt/")
    urlList.append("http://www.xicidaili.com/wn/")
    urlList.append("http://www.xicidaili.com/wt/")
    for url in urlList:
        natuals = itertools.count(1)
        ns = itertools.takewhile(lambda x: x <= 10, natuals)
        for i in list(ns):
            url= url+str(i)
            ipInfoList.extend(xicidailiSinglePage(url))
    #print(len(ipInfoList))  #todo
    return ipInfoList


def xicidailiSinglePage(url):
    ipInfoList = []
    #url = 'http://www.xicidaili.com/'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    for item in soup.select(".odd"):
        ipHost = item.find_all("td")
        ip = str(ipHost[2].string).strip()
        host = str(ipHost[3].string).strip()
        type = str(ipHost[6].string).strip()
        ipInfoList.append(IpInfo(ip, host, type=type))
        print("{0}:{1} {2}".format(ip, host, type))
    return ipInfoList


