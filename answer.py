#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xingjh

import os
import random
import subprocess
from io import BytesIO

import pytesseract
import requests
from PIL import Image

import baidu_api

config = {
    '头脑王者': {
        'title': (80, 500, 1000, 880),
        'answer': (80, 960, 1000, 1720),
        'points': [
            (316, 993, 723, 1078),
            (316, 1174, 723, 1292),
            (316, 1366, 723, 1469),
            (316, 1590, 723, 1657)
        ]
    }
}

# SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
SCREENSHOT_WAY = 2


def get_image():
    '''
    截取手机屏幕，获取图片
    :return:
    '''
    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        cmd = 'adb shell screencap -p'
        # os.system(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        screenout = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            screenout = screenout.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:
            screenout = screenout.replace(b'\r\r\n', b'\n')
        img_fb = BytesIO()
        img_fb.write(screenout)
        # with open('test1.png','wb') as f:
        #     f.write(screenout)
        # img = Image.open('test1.png')
        img = Image.open(img_fb)
    elif SCREENSHOT_WAY == 0:
        os.system('adb shell screencap -p /sdcard/answer.png')
        os.system('adb pull /sdcard/answer.png .')
        img = Image.open('answer.png')
    img_title = img.crop((80, 500, 1000, 880))
    img_answer = img.crop((80, 960, 1000, 1720))

    img_result = Image.new("RGBA", size=(920, 1140))
    img_result.paste(img_title, (0, 0, 920, 380))
    img_result.paste(img_answer, (0, 380, 920, 1140))

    new_img_fb = BytesIO()
    img_result.save(new_img_fb, 'png')
    return new_img_fb


def get_info(img):
    '''
    识别图片文字
    :param img:
    :return:
    '''
    words = baidu_api.image_to_str(img=img)
    return words


def analysis_answer(question, answers):
    '''
    百度问题，分析计算答案
    :param info:
    :return:
    '''
    url = 'https://www.baidu.com/s'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 '
                      'Safari/537.36'
    }
    data = {
        'wd': question
    }
    res = requests.get(url, params=data, headers=headers)
    res.encoding = 'utf-8'
    html = res.text

    for i in range(len(answers)):
        answers[i] = (html.count(answers[i]), answers[i], i)
    answers.sort(reverse=True)
    return answers


def do_click(point):
    '''
    根据答案排名，触发手机点击
    :param answer:
    :return:
    '''
    cmd = 'adb shell input swipe %s %s %s %s %s' % (
        point[0],
        point[1],
        point[0] + random.randint(0, 3),
        point[1] + random.randint(0, 3),
        random.randint(150, 220)
    )
    os.system(cmd)


def test_ocr():
    # tessdata_dir_config = '--tessdata-dir "D:\\software\\tesseract-ocr\\tessdata"'
    im = Image.open('44.jpg')
    # config=tessdata_dir_config
    print(pytesseract.image_to_string(im, lang='chi_sim'))


if __name__ == '__main__':
    input('请开始准备游戏')
    question_list = []
    # do_click(config['头脑王者']['points'][3])
    while True:
        print("开始答题：")
        image = get_image()
        info = get_info(image.getvalue())
        if info and len(info) > 4:
            answers = info[-4:]
            question = ''.join(info[:-4])
            if question in question_list:
                continue
            else:
                question_list.append(question)
                print('question: %s' % question)
                print('answer:$s' % answers)
                answer = analysis_answer(question, answers)
                print('answer: %s' % answer)
                print(config['头脑王者']['points'][answer[0][2]])
                do_click(config['头脑王者']['points'][answer[0][2]])
                # do_click(config['头脑王者']['points'][3])
                print("答题结束")
