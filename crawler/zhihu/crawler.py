#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

import aiohttp


async def fetch(client, url):
    print("crawler from :", url)
    #todo custom the connection
    async with client.get(url) as resp:
        assert resp.status == 200
        respContent = await resp.text()
        #todo handle response



print(aiohttp.ClientSession())
print(aiohttp.ClientSession())
with aiohttp.ClientSession() as client:
    print(client)


    asyncio.get_event_loop().run_until_complete(asyncio.wait([fetch(client), fetch2(client), fetch3(client)]))