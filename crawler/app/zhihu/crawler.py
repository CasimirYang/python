#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import logging.config
import yaml

from app.zhihu import User
from app.zhihu.crawlerHandle import init_session, handle_follow
from app.zhihu.dbUtil import get_user

yamlConfig = yaml.load(open(r'../../conf/loggingConfig.yaml', 'r'))
logging.config.dictConfig(yamlConfig)
logger = logging.getLogger(__name__)


def begin_to_crawler():
    session = init_session()
    user_list = get_user()
    if len(user_list) == 0:
        default_user = User('gong-zi-winnie', '心经', 1) #todo change to fetch from config
        handle_follow(session, default_user)
        user_list = get_user()
    i = 0
    print(len(user_list))
    while 1:
        i += 1
        logger.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  {0}  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^".format(i))
        if len(user_list) == 0 or i > 3:
            return #todo sent alert email

        #loop it
        for user in user_list:
            logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            user.status = 1
            handle_follow(session, user)
        user_list = get_user()


#begin_to_crawler()
# session = init_session()
# default_user = User('gong-zi-winnie', '心经', 1)
# handle_follow(session, default_user)
