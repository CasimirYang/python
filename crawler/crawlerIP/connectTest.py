#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from requests.packages.urllib3 import HTTPConnectionPool
from requests.packages.urllib3.exceptions import ConnectTimeoutError, MaxRetryError


def connectTest(ipInfoList):
    list = []
    httpUrl ='http://www.baidu.com'
    httpsUrl ='https://www.baidu.com'
    for ipInfo in ipInfoList:
        if str(ipInfo.type).lower() == 'http':
            proxy = 'http://{0}:{1}'.format(ipInfo.ip,ipInfo.host)
            proxies = {'http': proxy}
            url = httpUrl
        elif str(ipInfo.type).lower() == 'https':
            proxy = 'https://{0}:{1}'.format(ipInfo.ip,ipInfo.host)
            proxies = {'https': proxy}
            url = httpsUrl
        else:
            continue
        try:
            response = requests.head(url, proxies=proxies, timeout=5)
        except Exception as e:
            print("{ip}:{host} connect faild".format(ip=ipInfo.ip,host=ipInfo.host))
        else:
            if(response.status_code == 200):
                list.append(ipInfo)
                print("{ip}:{host} connect success !!".format(ip=ipInfo.ip,host=ipInfo.host))
    return list

