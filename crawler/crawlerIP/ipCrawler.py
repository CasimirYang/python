#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import logging.config
from crawlerIP.connectTest import connectTestAsync
from crawlerIP.dbUtil import saveToNeo
from crawlerIP.supplier import proxy360, xicidaili, bigdaili, youdaili

yamlConfig = yaml.load(open('../config/loggingConfig.yaml', 'r'))
logging.config.dictConfig(yamlConfig)


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



logger = logging.getLogger(__name__)
logger.info('begin to crawler IP')
ipCrawler()
logger.info('crawler IP finish.')




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

