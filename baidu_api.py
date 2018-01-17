#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xingjh

import base64
import json
from io import BytesIO
from urllib import parse, request

from PIL import Image


def get_image(path):
    im = Image.open(path)
    image_fb = BytesIO()
    im.save(image_fb, 'png')
    # print(image_fb.getvalue())
    return image_fb


def image_to_str(img):
    url = 'http://apis.baidu.com/idl_baidu/baiduocrpay/idlocrpaid'

    data = {}
    data['fromdevice'] = "pc"
    data['clientip'] = "10.10.10.0"
    data['detecttype'] = "LocateRecognize"
    data['languagetype'] = "CHN_ENG"
    data['imagetype'] = "1"


    # data['image'] = base64.b64encode(tmp)
    data['image'] = base64.b64encode(img)

    decoded_data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, data=decoded_data)

    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("apikey", "85de6391c6f159965c2ae795e66fd2ca")

    resp = request.urlopen(req)
    content = resp.read()
    if (content):
        retData = json.loads(content.decode('utf-8'))
        if retData and retData['errno'] == 0:
            words = [i['word'] for i in retData['retData']]
            return words

if __name__ == '__main__':
    im = get_image('221.jpg')
    words = image_to_str(im.getvalue())
    print(words)
