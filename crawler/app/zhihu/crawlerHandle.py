#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import logging.config
import aiohttp

import requests
import time
from bs4 import BeautifulSoup, SoupStrainer

from app.zhihu import User
from app.zhihu.dbUtil import save_user, save_followee, save_follower

logger = logging.getLogger(__name__)

headers={"Host": "www.zhihu.com",
         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36",
         "Referer": "http://www.zhihu.com/",
         "Origin": "http://www.zhihu.com"}

data={"remember_me": "true", "email": "tianxiaofu2@sina.com", "password": "txf1456123"}
proxy = "http://58.83.174.114:80"

async def loginByAiohttp():
    global cookies
    global proxy
    url= "http://www.zhihu.com/login/email"
    conn = aiohttp.ProxyConnector(proxy="http://58.83.174.114:80")
    client = aiohttp.ClientSession(connector=conn)
    try:
        async with client.post(url, headers=headers, data=data) as resp:
            cookies = resp.cookies
            print(await resp.json())
           # soup = BeautifulSoup(await resp.json(), "html.parser")
          #  print(soup.prettify())
    finally:
        client.close()

async def loginedTest():
    global cookies
    global proxy
    homePageUrl = "http://www.zhihu.com/people/tianxiaofu"
    conn = aiohttp.ProxyConnector(proxy="http://58.83.174.114:80")
    client = aiohttp.ClientSession(connector=conn)
    client._cookies=cookies
    print(cookies)
    try:
        async with client.get(homePageUrl, headers=headers) as resp:
            print(resp.status)
            print(await resp.test())
           # soup = BeautifulSoup(await resp.json(), "html.parser")
          #  print(soup.prettify())
    finally:
        client.close()


def loginByRequests():
    proxies = {'http': 'http://58.83.174.114:80'} #todo change to fetch from DB
    s = requests.Session()
    url = "http://www.zhihu.com/login/email"
    resp = requests.post(url, data=data, headers=headers, proxies=proxies)
    s.cookies = resp.cookies
    if resp.json()["msg"] == '登陆成功':
        logger.info("------------success to login -----------------") #log 支持中文？
    followees_PageUrl = "https://www.zhihu.com/people/tianxiaofu/followees"
    followees_Page = s.get(followees_PageUrl, proxies=proxies)
    soup = BeautifulSoup(followees_Page.text, "html.parser")
    print(soup)


def init_session():
    session = requests.Session()
    url = "http://www.zhihu.com/login/email"
    login_resp = requests.post(url, data=data, headers=headers)
    session.cookies.update(login_resp.cookies)
    if login_resp.json()["msg"] == '登陆成功':
        logger.info("-------------登陆成功-----------------")
    return session


def handle_follow(session, origin_user):
        logger.info("begin to handle user:{0}".format(origin_user.user_id))
        handle_follow_item(session, origin_user, 'ee')
        handle_follow_item(session, origin_user, 'er')


def handle_follow_item(session, origin_user, follow_type):
    global headers
    request_time = 0
    parse_time = 0
    user_list = [origin_user]
    homepage = "https://www.zhihu.com/people/{0}/follow{1}s".format(origin_user.user_id, follow_type)
    begin = time.time()
    homepage_soup = BeautifulSoup(session.get(homepage).text, "html.parser", from_encoding='UTF-8')
    end = time.time()
    print("spent {0} seconds to request and parse homePage.".format(end-begin))
    _xsrf = homepage_soup.find("input", attrs={'name': '_xsrf'})['value']
    div_text = homepage_soup.find("div", class_='zh-general-list clearfix')
    if div_text is None:
        save_user(user_list)
        return
    div_text = div_text['data-init']
    hash_id = json.loads(div_text)['params']['hash_id']
    followee_count = homepage_soup.find('div', class_='zm-profile-side-following zg-clear').select('strong')[0].text

    follow_url = "https://www.zhihu.com/node/ProfileFollow{0}sListV2".format(follow_type)
    headers["Referer"] = "http://www.zhihu.com/people/{0}/follow{1}s".format(origin_user.user_id, follow_type)
    params = {"order_by": "created", "offset": 0, "hash_id": hash_id}
    follow_data = {'_xsrf': _xsrf, 'method': 'next', 'params': ''}
    offset = 0
    print("following count:", str(followee_count))
    while offset < int(followee_count):
        params['offset'] = offset
        follow_data['params'] = json.dumps(params)
        begin = time.time()
        resp = session.post(follow_url, data=follow_data, headers=headers)
        end = time.time()
        spent_time = end-begin
        print("spent {0} seconds to request in FollowsList.".format(spent_time))
        request_time += spent_time
        try:
            soup = BeautifulSoup(str(resp.json()['msg']), "html.parser", from_encoding='UTF-8', parse_only=SoupStrainer("a", class_='zg-link'))
        except Exception:
            logger.info(str(resp.json()['msg']))
            logger.exception("------------------------------------------------------")
            return
        for item in soup.find_all('a'):
            href = item['href']
            user = User(href[href.rindex('/')+1:], item.text)
            user_list.append(user)
            #logger.info('fetch :{0}'.format(href))
        offset += 20
        end2 = time.time()
        spent_time = end2-end
        print("spent {0} seconds to parse html.".format(spent_time))
        parse_time += spent_time
        print("---------------------------------------each-------------------------------------------------")
    print("fetch {0} users to be saved.".format(len(user_list)))
    print("Summary: spent {0} seconds to request, {1} seconds to parse,".format(request_time, parse_time))
    save_user(user_list)
    user_list.remove(origin_user)
    if follow_type == 'ee':
        save_followee(origin_user, user_list)
    elif follow_type == 'er':
        save_follower(origin_user, user_list)
