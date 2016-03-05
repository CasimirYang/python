#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from py2neo import Graph, watch
from py2neo.cypher.error.schema import ConstraintViolation

from crawlerIP import IpInfo

watch("httpstream")  #The watch function comes with the bundled httpstream library and simply dumps log entries to standard output.
graph = Graph("http://neo4j:123456@localhost:7474/db/data/")
logger = logging.getLogger(__name__)

#graph.schema.create_uniqueness_constraint("IP", "ip")

def saveToNeo(ipInfoList):
    begin = time.time()
    transaction = graph.cypher.begin()
    statement = "MERGE (:IpInfo {ip:{ip},host:{host},user:{user},password:{password},type:{type},location:{location},time:{time}})"
    for ipInfo in ipInfoList:
        ip = ipInfo.ip
        host = ipInfo.host
        user = ipInfo.user
        password = ipInfo.password
        type = ipInfo.type
        location = ipInfo.location
        transaction.append(statement, {"ip": ip, "host": host, "user": user, "password": password, "type": type, "location": location, "time": time.time()})
        transaction.process()
    transaction.commit()
    end = time.time()
    logger.info("spent time:{0} to save {1} IPs.".format(end-begin, len(ipInfoList)))


def getIpInfoListFromNeo2():
    begin = time.time()
    ipInfoList = []
    ipInfo_Node_List = graph.cypher.execute("MATCH (IpList:IpInfo) RETURN IpList")
    for node in ipInfo_Node_List:
        ipInfo = IpInfo(node[0].properties["ip"], node[0].properties["host"])
        ipInfoList.append(ipInfo)
    end = time.time()
    logger.info("spent time:{0} to get ip from Neo.".format(end-begin))
    print(len(ipInfo_Node_List))
    return ipInfoList


def getIpInfoListFromNeo(limit=10):
    begin = time.time()
    ipInfoList = []
    ipInfo_Node_List = graph.find("IpInfo", limit=limit)
    for node in ipInfo_Node_List:
        ipInfo = IpInfo(node.properties["ip"], node.properties["host"])  #todo
        ipInfoList.append(ipInfo)
    end = time.time()
    logger.info("spent time:{0} to get {1} IPs from Neo.".format(end-begin, limit))
    return ipInfoList

