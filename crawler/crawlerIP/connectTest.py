#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

url ='http://www.baidu.com'
proxies = {
  'http': 'http://219.37.208.150:8080'
}
response = requests.get(url, proxies=proxies, timeout=5)
print(response.text)
