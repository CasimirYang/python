#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import os
import pickle

import aiohttp
import requests


list = []
logger = logging.getLogger(__name__)


def connectTest(ipInfoList):
    global list
    httpUrl = 'http://www.baidu.com'
    httpsUrl = 'https://www.baidu.com'
    for ipInfo in ipInfoList:
        if str(ipInfo.type).lower() == 'http':
            proxy = 'http://{0}:{1}'.format(ipInfo.ip, ipInfo.host)
            proxies = {'http': proxy}
            url = httpUrl
        elif str(ipInfo.type).lower() == 'https':
            proxy = 'https://{0}:{1}'.format(ipInfo.ip, ipInfo.host)
            proxies = {'https': proxy}
            url = httpsUrl
        else:
            continue
        try:
            response = requests.head(url, proxies=proxies, timeout=0.5)
        except Exception as e:
            logger.info("{ip}:{host} connect faild".format(ip=ipInfo.ip, host=ipInfo.host))
            logger.debug(e)
        else:
            if response.status_code == 200:
                list.append(ipInfo)
                logger.info("{ip}:{host} connect success !!".format(ip=ipInfo.ip, host=ipInfo.host))
    return list


def connectTestAsync(ipInfoList):
    global list
    list = []
    if len(ipInfoList) > 10:
        logger.warn("ipInfoList >10 !! ")
        return
    asyncio.get_event_loop().run_until_complete(asyncio.wait([fetch(ipInfo) for ipInfo in ipInfoList]))
    return list


async def fetch(ipInfo):
    with aiohttp.Timeout(1):
        global list
        #url = "http://www.zhihu.com"

        url = "https://www.zhihu.com/people/li-fang-quan-1/followers"

        proxy = "http://{ip}:{host}".format(type=ipInfo.type, ip=ipInfo.ip, host=ipInfo.host)
        logger.info("crawler from :{url} using:{proxy}".format(url=url, proxy=proxy))
        conn = aiohttp.ProxyConnector(proxy=proxy)
        client = aiohttp.ClientSession(connector=conn)

        file = open(os.path.join(os.path.dirname(__file__), "cookie.txt"), 'rb')
        cookies = pickle.load(file)
        file.close()
        client._cookies = cookies
        try:
            async with client.get(url) as resp:
                if resp.status == 200:
                    list.append(ipInfo)
                    logger.info("{ip}:{host} connect success !!".format(ip=ipInfo.ip, host=ipInfo.host))
        except Exception as e:
            logger.info("{ip}:{host} connect faild".format(ip=ipInfo.ip, host=ipInfo.host))
            logger.debug(e)
        finally:
            client.close()


def check_cn_ip(ip):
    country_id = 'TBC'
    url = "http://ip.taobao.com/service/getIpInfo.php?ip={0}".format(ip)
    response = requests.get(url)
    code = int(response.json()['code'])
    print(code)
    if code == 0:
        country_id = response.json()['data']["country_id"]
        print(country_id)
    return country_id

