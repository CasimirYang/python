#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from crawlerIP.connectTest import connectTestAsync
from crawlerIP.dbUtil import saveToNeo
from crawlerIP.supplier import proxy360, xicidaili, bigdaili, youdaili

raw_list = []
raw_list.extend(proxy360())
raw_list.extend(xicidaili())
raw_list.extend(bigdaili())
raw_list.extend(youdaili())
success_list = []
print(len(raw_list))
i = 0
while 1:
    if not len(raw_list) > i:
        break
    result_list = connectTestAsync(raw_list[i:i+10])
    if isinstance(result_list, list) and len(result_list) > 0:
        success_list.extend(result_list)
    i = i+10
print(len(success_list)) #todo change to log
print(success_list)
if len(success_list) > 0:
     saveToNeo(success_list)



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

