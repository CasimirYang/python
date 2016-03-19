#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import logging.config
import os
import pickle
import traceback

import aiohttp
import asyncio
import yaml

from app.zhihu import User, sent_email
from app.zhihu.crawlerHandle import init_session, handle_follow
from app.zhihu.dbUtil import get_user, get_total_user, get_total_relationshiop

logger = logging.getLogger()


def begin_to_crawler():
    global client
    file = open(os.path.join(os.path.dirname(__file__), "cookie.txt"), 'rb')
    cookies = pickle.load(file)
    file.close()
    client = aiohttp.ClientSession()
    client._cookies = cookies
   # session = init_session()
    user_list = get_user()
    if len(user_list) == 0:
        default_user = User('gong-zi-winnie', '心经', 1) #todo change to fetch from config
        handle_follow(client, default_user)
        user_list = get_user()
    i = 0
    while 1:
        i += 1
        logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  {0} cycle. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(i))
        #loop it
        #for user in user_list:
            #user.status = 1
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait([handle_follow(user) for user in user_list]))
        loop.close()
           # handle_follow(client, user)

        if len(user_list) == 0:
            logger.info("crawler done.")
            # total_user = get_total_user()
            # total_rela = get_total_relationshiop()
            # sent_email("Crawler Info", "crawler done.<br /> "
            #                            "Summary: total user:{0} total relationship:{1}".format(total_user, total_rela))
            return

        user_list = get_user()


def zhihu_crawler():
    try:
        begin_to_crawler()
    except Exception:
        logger.exception("crawler zhihu cause exception.")
        #sent_email("Crawler Exception. detmail:<br />", traceback.format_exc())



if __name__=='__main__':
    yamlConfig = yaml.load(open(r'../../conf/test.yaml', 'r'))
    logging.config.dictConfig(yamlConfig)
    zhihu_crawler()
    # session = init_session()
    # default_user = User('jingyi-liu-11', 'jingyi liu', 1)
    # handle_follow(session, default_user)



