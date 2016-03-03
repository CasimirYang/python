#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

import aiohttp

from crawlerIP import IpInfo

list = []

async def fetch(ipInfo):
    global list
    url = "{0}://www.baidu.com".format(ipInfo.type)
    proxy = "{type}://{ip}:{host}".format(type=ipInfo.type, ip=ipInfo.ip, host=ipInfo.host)
    print("crawler from :{url} using:{proxy}".format(url=url, proxy=proxy))
    conn = aiohttp.ProxyConnector(proxy=proxy)
    client = aiohttp.ClientSession(connector=conn)
    #todo custom the connection
    try:
        async with client.get(url) as resp:
            if resp.status == 200:
                list.append(ipInfo)
                print("{ip}:{host} connect success !!".format(ip=ipInfo.ip, host=ipInfo.host))
    except Exception as e:
        print("{ip}:{host} connect faild".format(ip=ipInfo.ip, host=ipInfo.host))
        print(e)
        #todo log e


def connectTest(ipInfoList):
    if len(ipInfoList) > 10:
        raise ImportWarning("ipInfoList >10 !! ")
    asyncio.get_event_loop().run_until_complete(asyncio.wait([fetch(ipInfo) for ipInfo in ipInfoList]))
    return list

# ipInfoList=[]
# ipInfoList.append(IpInfo("125.102.112.101", "7878"))
# ipInfoList.append(IpInfo("125.102.102.101", "8081"))
# connectTest(ipInfoList)