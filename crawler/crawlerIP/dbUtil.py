#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time


from py2neo import Graph, Node, Relationship, watch
from py2neo.cypher.error.schema import ConstraintViolation

watch("httpstream")  #The watch function comes with the bundled httpstream library and simply dumps log entries to standard output.

graph = Graph("http://neo4j:123456@localhost:7474/db/data/")
#graph.schema.create_uniqueness_constraint("IP", "ip")


def saveToNeo(ipHostList):
    begin = time.time()
    transaction = graph.cypher.begin()
    statement = "CREATE (:IP {ip:{ip},host:{host},time:{time}})"
    for ipHost in ipHostList:
        ipHost = ipHost.split(":")
        ip = ipHost[0]
        host = ipHost[1]
        transaction.append(statement, {"ip": ip, "host": host, "time": time.time()})
        try:
            transaction.process()
        except ConstraintViolation as e:
            print(e)
            logging.
    transaction.commit()
    end = time.time()
    print("spent time:{0}".format(end-begin))

ipHostList = ["13.152.21.112:8080", "13.101.45.211:6565", "103.125.1.125:7474", "123.18.10.122:8181"]
saveToNeo(ipHostList)

