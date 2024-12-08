import os
import time
import hashlib
import hmac
import base64
import uuid
import requests

SWITCHBOT_HOST = "https://api.switch-bot.com"


def gen_header():
    # Declare empty header dictionary
    apiHeader = {}
    # open token
    token = os.environ.get("SWITCHBOT_TOKEN")
    secret = os.environ.get("SWITCHBOT_SECRET")
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    apiHeader['Authorization'] = token
    apiHeader['Content-Type'] = 'application/json'
    apiHeader['charset'] = 'utf8'
    apiHeader['t'] = str(t)
    apiHeader['sign'] = str(sign, 'utf-8')
    apiHeader['nonce'] = str(nonce)
    return apiHeader


def request(method, path):
    url = SWITCHBOT_HOST + path
    headers = gen_header()
    response = requests.request(method, url, headers=headers)
    return response.json()

