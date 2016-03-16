#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import logging
import smtplib
import time
import traceback
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr


class User(object):
    __slots__ = ('user_id', 'user_name', 'status')

    def __init__(self, user_id, user_name, status=0):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name
        self.status = status


class UserDetail(object):

    """
    static:
    0: new one.
    1: handling
    2:handle done.
"""
    __slots__ = ('xsrf', 'hash_id', 'followee_count', 'follower_count')

    def __init__(self, xsrf, hash_id, followee_count, follower_count):
        super().__init__()
        self.xsrf = xsrf
        self.hash_id = hash_id
        self.followee_count = followee_count
        self.follower_count = follower_count


logger = logging.getLogger(__name__)


def log_time(param):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            spent_time = end - start
            logger.info("spend {0} seconds to {1} ".format(spent_time, param))
            return result
        return wrapper
    return decorator


def sent_email(mess, tittle="Cralwer Alert"):
    mess = "<html><body>{0}</body></html>".format(mess)
    sent = "tianxiaofu2@sina.com"
    server = smtplib.SMTP("smtp.sina.com", 25)
    server.set_debuglevel(1)
    server.login(sent, "txf1456123")
    msg = MIMEText(mess, 'html', 'utf-8')
    msg['From'] = formataddr((Header("Crawler", 'utf-8').encode(), sent))
    msg['Subject'] = Header(tittle, 'utf-8').encode()
    server.sendmail("tianxiaofu2@sina.com", ["704360537@qq.com"], str(msg))
    server.quit()


