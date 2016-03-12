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



def begin_to_crawler():
    session = init_session()
    user_list = get_user()
    if len(user_list) == 0:
        default_user = User('alexya', 'ALEX YA', 'true') #todo change to fetch from config
        handle_follow(session, default_user)
        user_list = get_user()
    i = 0
    print(len(user_list))
    while 1:
        i += 1
        if len(user_list) == 0 or i > 20:
            return #todo sent alert email

        #loop it
        for user in user_list:
            user.have_disposed = 'true'
            handle_follow(session, user )


# begin_to_crawler()
session = init_session()
default_user = User('Ace1987', '张兆杰', 'true') #todo change to fetch from config
handle_follow(session, default_user)
