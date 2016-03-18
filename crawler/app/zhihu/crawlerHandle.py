#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import logging.config
import os
import pickle
import traceback

import aiohttp
import asyncio
import requests
import time

import tornado
from requests import RequestException
from bs4 import BeautifulSoup, SoupStrainer

from app.crawlerIP.dbUtil import get_proxy_ip_host
from app.zhihu import User, UserDetail, log_time, sent_email
from app.zhihu.dbUtil import save_user, save_follow, update_user_status

logger = logging.getLogger(__name__)

headers = {"Host": "www.zhihu.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36",
           "Referer": "http://www.zhihu.com/",
           "Origin": "http://www.zhihu.com",
           "accept-encoding": "gzip, deflate"
           }

data = {"remember_me": "true", "email": "tianxiaofu3@sina.com", "password": "txf1456123"}
proxy = {"http": "http://58.83.174.114:80"}

func = get_proxy_ip_host()


def get_proxy():
    # default_proxy = {"http": "http://58.83.174.114:80"}
    ip, host = func.__next__()
    return {"http": "http://{0}:{1}".format(ip, host)}


async def loginByAiohttp():
    global client
    global cookie
    data = {"remember_me": "true", "email": "tianxiaofu2@sina.com", "password": "txf1456123"}
    url = "http://www.zhihu.com/login/email"
    conn = aiohttp.ProxyConnector(proxy="http://119.39.191.52:80")
    client = aiohttp.ClientSession()
    resp = await client.post(url, headers=headers, data=data)
    cookie = client.cookies
    file = open(os.path.join(os.path.dirname(__file__), "cookie.txt"), 'wb')
    pickle.dump(cookie, file)
    file.close()
    print("cookie:{0}".format(cookie))
    print(await resp.json())

    url2 = "http://www.zhihu.com/people/li-fang-quan-1/followers"
    resp = await client.get(url2)
    print(await resp.text())

async def test(client):
    print("test1")
    homePageUrl = "https://www.zhihu.com/people/li-fang-quan-1/followers"
    resp = await client.get(homePageUrl)
    print("test2")
    print(await resp.text())

async def test2(client):
    print("test1")
    homePageUrl = "https://www.zhihu.com/people/li-fang-quan-1/followers"
    resp = await client.get(homePageUrl)
    print("test2")
    print(await resp.text())


if __name__=='__main__':
    file = open(os.path.join(os.path.dirname(__file__), "cookie.txt"), 'rb')
    cookies = pickle.load(file)
    file.close()
    conn = aiohttp.ProxyConnector("http://222.176.112.10:80")
    client = aiohttp.ClientSession(connector=conn, headers=headers)
    client._cookies = cookies
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([test(client), test2(client)]))



def init_session():
    session = requests.Session()
    url = "http://www.zhihu.com/login/email"
    login_resp = requests.post(url, data=data, headers=headers)
    session.cookies.update(login_resp.cookies)
    if login_resp.json()["msg"] == '登陆成功':
        logger.info("-------------登陆成功-----------------")
    else:
        logger.info(login_resp.json()["msg"])
    return session


@log_time("handle follow.")
def handle_follow(session, origin_user):
    logger.info("begin to handle user:{0}".format(origin_user.user_id))
    update_user_status(origin_user, 1)
    item_flag = 0
    while 1:
        item_flag += 1
        try:
            handle_follow_item(session, origin_user, 'ee')
        except Exception as e:
            sent_email("Crawler Exception. handle_followee_item :<br />", traceback.format_exc())
            logger.exception("retry {0}. time:".format("handle_followee_item", item_flag))
            if item_flag > 5:
                raise e
            else:
                continue
        else:
            item_flag = 0
            break
    while 1:
        item_flag += 1
        try:
            handle_follow_item(session, origin_user, 'er')
        except Exception as e:
            sent_email("Crawler Exception. handle_follower_item :<br />", traceback.format_exc())
            logger.exception("retry {0}. time:".format("handle_follower_item", item_flag))
            if item_flag > 5:
                raise e
            else:
                continue
        else:
            break
    update_user_status(origin_user, 2)


@log_time("handle follow item.")
def handle_follow_item(session, origin_user, follow_type):
    global headers
    user_list = [origin_user]
    homepage = "http://www.zhihu.com/people/{0}/follow{1}s".format(origin_user.user_id, follow_type)
    user_detail = get_user_detail(session, homepage)
    logger.info("followee count:{0},follower count:{1} ".format(str(user_detail.followee_count),
                                                                str(user_detail.follower_count)))
    if follow_type == 'ee':
        follow_count = int(user_detail.followee_count)
    else:
        follow_count = int(user_detail.follower_count)
    if follow_count != 0:
        follow_url = "http://www.zhihu.com/node/ProfileFollow{0}sListV2".format(follow_type)
        headers["Referer"] = "http://www.zhihu.com/people/{0}/follow{1}s".format(origin_user.user_id, follow_type)
        params = {"order_by": "created", "offset": 0, "hash_id": user_detail.hash_id}
        follow_data = {'_xsrf': user_detail.xsrf, 'method': 'next', 'params': ''}
        iterator_flag = 0
        offset = 0
        while offset < follow_count:
            logger.info("begin to do offset:{0}".format(offset))
            session.proxies = {}
            params['offset'] = offset
            follow_data['params'] = json.dumps(params)
            resp = get_response(session, follow_url, follow_data, headers)
            soup = BeautifulSoup(str(resp.json()['msg']), "html.parser", from_encoding='UTF-8',
                                 parse_only=SoupStrainer("a", class_='zg-link'))
            for item in soup.find_all('a'):
                href = item['href']
                user = User(href[href.rindex('/') + 1:], item.text)
                user_list.append(user)
            offset += 20
            iterator_flag += 20
            if iterator_flag == 1000 or offset >= follow_count:
                save_user(user_list)
                if origin_user in user_list:
                    user_list.remove(origin_user)
                save_follow(origin_user, user_list, follow_type)
                user_list.clear()
                iterator_flag = 0


@log_time("request and parse homePage.")
def get_user_detail(session, homepage):
    resp = get_response(session, homepage, None, None, 'get')
    homepage_soup = BeautifulSoup(resp.text, "html.parser", from_encoding='UTF-8')
    xsrf = homepage_soup.find("input", attrs={'name': '_xsrf'})['value']
    div_text = homepage_soup.find("div", class_='zh-general-list clearfix')
    if div_text is None:
        hash_id = -1
    else:
        div_text = div_text['data-init']
        hash_id = json.loads(div_text)['params']['hash_id']
    followee_count = homepage_soup.find('div', class_='zm-profile-side-following zg-clear').select('strong')[0].text
    follower_count = homepage_soup.find('div', class_='zm-profile-side-following zg-clear').select('strong')[1].text
    return UserDetail(xsrf, hash_id, followee_count, follower_count)


@log_time("get response.")
def get_response(session, follow_url, follow_data, headers, request_type='post'):
    retry_flag = 1
    while 1:
        retry_flag += 1
        if retry_flag > 20:  #todo max retry time : 20 ip
            logger.error("retry max time. ")
            raise IOError("retry max time. ")
        try:
            if request_type == 'get':
                resp = session.get(follow_url, data=follow_data, headers=headers, timeout=60)
            else:
                resp = session.post(follow_url, data=follow_data, headers=headers, timeout=60)
            if resp.status_code != 200:
                logger.error("error status:{0}".format(resp.status_code))
                #time.sleep(5)
                session.proxies = get_proxy()
            else:
                return resp
        except RequestException:
            logger.exception("get offset response exception.")
            #time.sleep(5)
            session.proxies = get_proxy()