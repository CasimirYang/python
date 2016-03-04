#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from crawlerIP.connectTest import connectTestAsync
from crawlerIP.dbUtil import saveToNeo
from crawlerIP.supplier import proxy360, xicidaili, bigdaili, youdaili


class IpInfo(object):
    __slots__ = ('ip', 'host', 'user', 'password', 'type', 'location') # 用tuple定义允许绑定的属性名称

    def __init__(self, ip, host, user='', password='', type='http', location='CN'):
        self.ip = ip
        self.host = host
        self.user = user
        self.password = password
        self.type = type
        self.location = location  #todo @property


logger = logging.getLogger(__name__)


def ipCrawler():
    raw_list = []
    try:
        raw_list.extend(proxy360())
    except Exception as e:
        logger.warn("Catch error when fetch ip from proxy360.")
        logger.warn(e)
    try:
        raw_list.extend(xicidaili())
    except Exception as e:
        logger.warn("Catch error when fetch ip from xicidaili.")
        logger.warn(e)
    try:
        raw_list.extend(bigdaili())
    except Exception as e:
        logger.warn("Catch error when fetch ip from bigdaili.")
        logger.warn(e)
    try:
        raw_list.extend(youdaili())
    except Exception as e:
        logger.warn("Catch error when fetch ip from youdaili.")
        logger.warn(e)

    success_list = []
    logger.info("-------------fetch raw {0} IPs in this job------------".format(len(raw_list)))

    i = 0
    while 1:
        if not len(raw_list) > i:
            break
        result_list = connectTestAsync(raw_list[i:i+10])
        if isinstance(result_list, list) and len(result_list) > 0:
            success_list.extend(result_list)
        i = i+10
    logger.info("After connect test, there are {count} IP in this job.".format(count=len(success_list)))
    if len(success_list) > 0:
         saveToNeo(success_list)

