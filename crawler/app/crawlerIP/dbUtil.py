#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from py2neo import Graph

from app.crawlerIP import IpInfo
from app.crawlerIP.connectTest import check_cn_ip, connectTestAsync

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
    getIp = lambda: graph.cypher.execute("MATCH (ipInfo:IpInfo) WHERE ipInfo.location='CN' RETURN ipInfo")
    # = graph.cypher.execute("MATCH (ipInfo:IpInfo) WHERE ipInfo.location='CN' RETURN ipInfo")
    while 1:
        ip_list = getIp()
        for record in ip_list:
            graph.find_one(label="IpInfo", property_key="location", property_value="CN")
            ip, host = record['ipInfo'].properties["ip"], record['ipInfo'].properties["host"]
            yield ip, host


if __name__=='__main__':

    list2 = get_proxy_ip_host()
    raw_list = []
    for i2 in list2:
        ip, host = i2['ipInfo'].properties["ip"], i2['ipInfo'].properties["host"]
        raw_list.append(IpInfo(ip, host))
    success_list =[]
    i = 0
    while 1:
        if not len(raw_list) > i:
            break
        result_list = connectTestAsync(raw_list[i:i+10])
        if isinstance(result_list, list) and len(result_list) > 0:
            for item in result_list:
                print("{0}:{1}".format(item.ip,item.host))
            success_list.extend(result_list)
        i += 10
    print(len(success_list))
#
# 123.126.108.190:3128
# 45.113.253.45:8090
# 115.25.138.245:3128
# 45.113.253.43:8090
# 45.113.253.43:8090
# 45.113.253.45:8090
# 111.161.126.107:80
# 101.226.249.237:80
# 101.200.181.36:3128
# 58.211.13.26:55336
# 61.160.250.25:3128
# 101.226.249.237:80
# 61.160.250.25:3128
# 45.113.253.43:8090
# 45.113.253.45:8090
# 45.113.253.43:8090
# 45.113.253.45:8090
# 222.176.112.10:80
# 45.113.253.43:8090
# 119.147.161.55:3128
# 101.200.179.38:3128
# 101.200.178.46:3128
# 61.160.250.25:3128
# 61.160.250.25:3128
# 61.160.250.25:3128
    # func = get_proxy_ip_host()
    # for i in func:
    #     print(i.__len__())
    #     print(func.send(None))
    #     print(func.__next__())
    #     print(func.send(None))
