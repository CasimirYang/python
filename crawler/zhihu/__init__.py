#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from asyncio import sleep

import aiohttp

# async def hello():
#     print("Hello world!")
#     r = await sleep(1)
#     print("Hello again!")

async def getResponse(session):
    resp = session.get('https://api.github.com/events')
    print(resp.status)
    print(await resp.text())


async def fetch(client):
    print("get from :", "baidu")
    async with client.get('http://www.baidu.com') as resp:
        assert resp.status == 200
        print(await resp.text())

async def fetch2(client):
    print("get from :", "readthedocs")
    async with client.get('http://aiohttp.readthedocs.org/en/stable/client_reference.html') as resp:
        assert resp.status == 200
        print(await resp.text())

async def fetch3(client):
    print("get from :", "jobbole")
    async with client.get('http://blog.jobbole.com/63897/') as resp:
        assert resp.status == 200
        print(await resp.text())

with aiohttp.ClientSession() as client:
    asyncio.get_event_loop().run_until_complete(asyncio.wait([fetch(client), fetch2(client), fetch3(client)]))