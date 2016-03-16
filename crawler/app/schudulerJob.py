#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.tornado import TornadoScheduler

from app.crawlerIP.ipCrawler import ip_crawler
from app.zhihu.crawler import zhihu_crawler

scheduler = TornadoScheduler()

def ip_schuduler():
    scheduler._logger = logging.getLogger('apscheduler.scheduler')
    scheduler.add_job(ip_crawler, 'interval', days=1) #need zhihu_scheduler stop to run
    scheduler.start()


def zhihu_scheduler():
    scheduler._logger = logging.getLogger('apscheduler.scheduler')
    scheduler.add_job(zhihu_crawler)
    scheduler.start()


def start_schuduler():
    #ip_schuduler()
    zhihu_scheduler()


def stop_scheduler(wait=False):
    scheduler.shutdown(wait=wait)