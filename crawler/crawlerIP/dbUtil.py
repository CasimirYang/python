#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from py2neo import Graph, watch
from py2neo.cypher.error.schema import ConstraintViolation

from crawlerIP import IpInfo

watch("httpstream")  #The watch function comes with the bundled httpstream library and simply dumps log entries to standard output.
graph = Graph("http://neo4j:123456@localhost:7474/db/data/")

#graph.schema.create_uniqueness_constraint("IP", "ip")

def saveToNeo(ipInfoList):
    begin = time.time()
    transaction = graph.cypher.begin()
    statement = "CREATE (:IpInfo {ip:{ip},host:{host},user:{user},password:{password},type:{type},location:{location},time:{time}})"
    for ipInfo in ipInfoList:
        ip = ipInfo.ip
        host = ipInfo.host
        user = ipInfo.user
        password = ipInfo.password
        type = ipInfo.type
        location = ipInfo.location
        transaction.append(statement, {"ip": ip, "host": host, "user": user, "password": password, "type": type, "location": location, "time": time.time()})
        try:
            transaction.process()
        except ConstraintViolation as e:
            print(e) #todo
    transaction.commit()
    end = time.time()
    print("spent time:{0}".format(end-begin)) #todo


def getIpInfoListFromNeo2():
    time1 = time.time()
    ipInfoList = []
    ipInfo_Node_List = graph.cypher.execute("MATCH (IpList:IpInfo) RETURN IpList")
    for node in ipInfo_Node_List:
        ipInfo = IpInfo(node[0].properties["ip"], node[0].properties["host"])
        ipInfoList.append(ipInfo)
    time2 = time.time()
    print(time2-time1)
    print(len(ipInfo_Node_List))
    return ipInfoList


def getIpInfoListFromNeo():
    time1 = time.time()
    ipInfoList = []
    ipInfo_Node_List = graph.find("IpInfo")
    for node in ipInfo_Node_List:
        ipInfo = IpInfo(node.properties["ip"], node.properties["host"])  #todo
        ipInfoList.append(ipInfo)
    time2 = time.time()
    print(time2-time1)
    return ipInfoList

