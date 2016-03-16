#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import logging.config
import traceback

from app.zhihu import User, sent_email
from app.zhihu.crawlerHandle import init_session, handle_follow
from app.zhihu.dbUtil import get_user, get_total_user, get_total_relationshiop

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
        if len(user_list) == 0:
            logger.info("crawler done.")
            total_user = get_total_user()
            total_rela = get_total_relationshiop()
            sent_email("Crawler Info", "crawler done.<br /> "
                                       "Summary: total user:{0} total relationship:{1}".format(total_user, total_rela))
            return

        #loop it
        for user in user_list:
            user.status = 1
            handle_follow(session, user)
        user_list = get_user()


def zhihu_crawler():
    try:
        begin_to_crawler()
    except Exception:
        logger.exception("crawler zhihu cause exception.")
        sent_email("Crawler Exception. detmail:<br /> {0}", traceback.format_exc())



