#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from py2neo import Graph

from app.crawlerIP import IpInfo
from app.crawlerIP.connectTest import check_cn_ip

graph = Graph("http://neo4j:123456@localhost:7474/db/data/")
logger = logging.getLogger(__name__)


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


def locate_ip_country():
    while 1:
        ip_list = graph.cypher.execute("MATCH (ipInfo:IpInfo) WHERE"
                                                " ipInfo.location='empty' RETURN ipInfo limit 10")
        if len(ip_list) == 0:
            return
        for record in ip_list:
            ip = record["ipInfo"].properties["ip"]
            print(ip)
            country_id = check_cn_ip(ip)
            if country_id != 'TBC':
                statement = "MATCH (ip:IpInfo{ip:{ip}}) SET ip.location={location}"
                graph.cypher.execute(statement, {"ip": ip, "location": country_id})
            time.sleep(0.2)


def get_proxy_ip_host():
    ip_list = graph.cypher.execute("MATCH (ipInfo:IpInfo) WHERE ipInfo.location='CN' RETURN ipInfo limit 100")
    for record in ip_list:
        graph.find_one(label="IpInfo", property_key="location", property_value="CN")
        ip, host = record['ipInfo'].properties["ip"], record['ipInfo'].properties["host"]
        yield ip, host
