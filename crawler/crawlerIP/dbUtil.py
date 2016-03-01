#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

import requests
from py2neo import Graph, watch
from py2neo.cypher.error.schema import ConstraintViolation

watch("httpstream")  #The watch function comes with the bundled httpstream library and simply dumps log entries to standard output.
graph = Graph("http://neo4j:123456@localhost:7474/db/data/")

#graph.schema.create_uniqueness_constraint("IP", "ip")

def saveToNeo(ipInfoList):
    begin = time.time()
    transaction = graph.cypher.begin()
    statement = "CREATE (:IP2 {ip:{ip},host:{host},user:{user},password:{password},type:{type},location:{location},time:{time}})"
    for ipInfo in ipInfoList:
        ip = ipInfo.ip
        host = ipInfo.host
        user = ipInfo.user
        password = ipInfo.password
        type = ipInfo.type
        location = ipInfo.location
        transaction.append(statement, {"ip": ip, "host": host, "user": user, "password": password,"type": type,"location":location, "time": time.time()})
        try:
            transaction.process()
        except ConstraintViolation as e:
            print(e) #todo
    transaction.commit()
    end = time.time()
    print("spent time:{0}".format(end-begin)) #todo



