#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
http://www.youdaili.net
http://www.proxy360.cn/Proxy
http://www.xicidaili.com/
http://ip.zdaye.com/dayProxy/2016/3/1.html
https://www.imfreevpn.com/
"""

import itertools
import logging
import re

import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import HTTPError

from crawlerIP import IpInfo

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'}
logger = logging.getLogger(__name__)



def proxy360():
    ipInfoList = []
    url = 'http://www.proxy360.cn/Proxy'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for item in soup.select(".proxylistitem"):
        ipHost = item.find("div").find_all("span", limit=2)
        ip = str(ipHost[0].string).strip()
        host = str(ipHost[1].string).strip()
        ipInfoList.append(IpInfo(ip, host))
        logger.info("fetch {0} IPs from www.proxy360.cn".format(len(ipInfoList)))
    return ipInfoList


def xicidaili():
    ipInfoList = []
    urlList = []
    urlList.append("http://www.xicidaili.com/nn/")
    urlList.append("http://www.xicidaili.com/nt/")
    urlList.append("http://www.xicidaili.com/wn/")
    urlList.append("http://www.xicidaili.com/wt/")
    for url in urlList:
        natuals = itertools.count(1)
        ns = itertools.takewhile(lambda x: x <= 10, natuals)
        for i in list(ns):
            url= url+str(i)
            ipInfoList.extend(xicidailiItem(url))
    logger.info("fetch {0} IPs from www.xicidaili.com".format(len(ipInfoList)))
    return ipInfoList


def xicidailiItem(url):
    ipInfoList = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    for item in soup.select(".odd"):
        ipHost = item.find_all("td")
        ip = str(ipHost[2].string).strip()
        host = str(ipHost[3].string).strip()
        type = str(ipHost[6].string).strip()
        ipInfoList.append(IpInfo(ip, host, type=type))
    return ipInfoList

def zdaye():
    ipInfoList = []
    url = "http://ip.zdaye.com/dayProxy/2016/3/1.html"
    cookies = {"cf_clearance": "7883097748f99d85c974890303c6307cd9cd4aca-1457012666-1800"}
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.status_code)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.text)
    for item in soup.select(".title"):
        href = "http://ip.zdaye.com{0}".format(item.a["href"])
        ipInfoList.extend(zdaygItem(href))
    return ipInfoList


def zdaygItem(url):
    ipInfoList = []
    cookies = {"cf_clearance" : "7883097748f99d85c974890303c6307cd9cd4aca-1457012666-1800"}
    response = requests.get(url, headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.text)
    for br in soup.find(".cont").br:
        ipHost = str(br.text).strip()
        print(ipHost)
        print(re.match('d+\.d+\.d+\.d+:d+', ipHost).groups(0))
        #ipInfoList.append(IpInfo(ip, host, type=type))
        #print("{0}:{1} {2}".format(ip, host, type))
    return ipInfoList


def bigdaili():
    ipInfoList = []
    for i in range(1, 5):
        for j in range(1, 11):
            url = "http://www.bigdaili.com/dailiip/{0}/{1}.html#ip".format(i, j)
            ipInfoList.extend(bigdailiItem(url))
    logger.info("fetch {0} IPs from www.bigdaili.com".format(len(ipInfoList)))
    return ipInfoList


def bigdailiItem(url):
    ipInfoList = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    for tr in soup.select(".segment tbody tr"):
        ipHost = tr.find_all("td", limit=2)
        ip = str(ipHost[0].string).strip()
        host = str(ipHost[1].string).strip()
        ipInfoList.append(IpInfo(ip, host))
    return ipInfoList

def youdaili():
    ipInfoList = []
    url = "http://www.youdaili.net"
    linkList = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    re_sameDomain = re.compile(r'^http://www\.youdaili\.net/Daili[^s]*html')
    for link in soup.find_all('a'):
        link = link.get('href')
        if(link != None and re_sameDomain.match(link)):
            linkList.append(link)
    for url in linkList:
        response = requests.get(url)
        if(response.status_code == 200):
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                for p in soup.select(".cont_font p"):
                    for item in str(p).split("<br/>"):
                        ipHost = re.match("\d+\.\d+\.\d+\.\d+:\d+", str(item).strip())
                        if ipHost is not None:
                            ipHost = ipHost.group(0).split(":")
                            ipInfoList.append(IpInfo(ipHost[0], ipHost[1]))
            except AttributeError as e:
                logger.debug(e)
    logger.info("fetch {0} IPs from www.youdaili.net".format(len(ipInfoList)))
    return ipInfoList
