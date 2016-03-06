#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.config

import yaml
from crawlerIP.dbUtil import saveToNeo
from crawlerIP.supplier import proxy360, xicidaili, bigdaili, youdaili

from app.crawlerIP.connectTest import connectTestAsync

yamlConfig = yaml.load(open('../conf/loggingConfig.yaml', 'r'))
logging.config.dictConfig(yamlConfig)

logger = logging.getLogger(__name__)


def ipCrawler():
    logger.info('begin to crawler IP')
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

    j = 0
    while 1:
        if not len(success_list) > j:
            break
        result_list = success_list[j:j+100]
        if isinstance(result_list, list) and len(result_list) > 0:
            saveToNeo(result_list)
        j = j+100
    logger.info('crawler IP finish.')