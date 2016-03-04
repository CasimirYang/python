#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import logging.config
import crawlerIP


yamlConfig = yaml.load(open('../config/loggingConfig.yaml', 'r'))
logging.config.dictConfig(yamlConfig)


logger = logging.getLogger(__name__)
logger.info('begin to crawler IP')
crawlerIP.ipCrawler()
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

