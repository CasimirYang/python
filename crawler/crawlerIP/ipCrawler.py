#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from requests_futures.sessions import FuturesSession

from crawlerIP.connectTest import connectTest
from crawlerIP.dbUtil import saveToNeo, getIpInfoListFromNeo
from crawlerIP.supplier import proxy360, xicidaili


IP_INFOList = connectTest(proxy360())
print(len(IP_INFOList))
if len(IP_INFOList) > 0:
    saveToNeo(IP_INFOList)


IP_INFOList = connectTest(xicidaili())
print(len(IP_INFOList))
if len(IP_INFOList) > 0:
    saveToNeo(IP_INFOList)





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

session = FuturesSession()