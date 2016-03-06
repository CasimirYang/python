#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.tornado import TornadoScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())


def schudulerStart():
    scheduler = TornadoScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    # todo add a new job to validate exist IP
    scheduler.start()