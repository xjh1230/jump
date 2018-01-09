#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xingjh

import os
import PIL, numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import time

need_updata = True

def set_button_position(im):
    """
    将 swipe 设置为 `再来一局` 按钮的位置
    """
    global swipe_x1, swipe_y1, swipe_x2, swipe_y2
    w, h = im.size
    left = int(w / 2)
    top = int(1584 * (h / 1920.0))
    left = int(random.uniform(left-50, left+50))
    top = int(random.uniform(top-10, top+10))    # 随机防 ban
    swipe_x1, swipe_y1, swipe_x2, swipe_y2 = left, top, left, top

	

def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screen.png')
    os.system('adb pull /sdcard/screen.png')
    im=PIL.Image.open('screen.png')
    set_button_position(im)
    return numpy.array(im)


def jump_to_next(point1, point2):
    x1, y1 = point1;
    x2, y2 = point2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    os.system('adb shell input swipe {} {} {} {} {}'.format(swipe_x1,swipe_y1,swipe_x2,swipe_y2,int(distance * 1.35)))
    # os.system('adb shell input swipe {} {} {} {} {}'.format(320, 410, 320, 410, int(distance * 1.35)))
    # os.system('adb shell input swipe 320 410 320 410 {}'.format(int(distance * 1.35)))

def on_click(event, coor=[]):
    global need_updata
    coor.append((event.xdata, event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(), coor.pop())
        need_updata = True


def update_screen(frame):
    # print(frame)
    global need_updata
    if need_updata:
        time.sleep(1)
        axes_img.set_array(get_screen_image())
        need_updata = False
    return axes_img,


if __name__ == '__main__':
    # print(os.system('ipconfig'))
    figure = plt.figure()  # 创建一张空白画布
    axes_img = plt.imshow(get_screen_image(), animated=True)  # 把获取到的图片打印到坐标轴上
    figure.canvas.mpl_connect('button_press_event', on_click)
    ani = FuncAnimation(figure, update_screen, interval=50, blit=True)
    plt.show()
