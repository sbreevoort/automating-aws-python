# coding: utf-8
import requests
url = '' #secret
data = {"text": "Hello world!"}

requests.post(url, json=data)
