# coding = utf-8
"""
@author: zhou
@time:2019/3/23 13:10
"""

import time
from threading import Timer
import json


def dingshi1():
    while True:
        print("time", time.localtime())
        time.sleep(3)


def dingshi2_1():
    print("2-1 time: ", time.localtime())
    t = Timer(3, dingshi2_1)
    t.start()


def dingshi2_2():
    print("2-2 time: ", time.localtime())
    t = Timer(1, dingshi2_2)
    t.start()


from apscheduler.schedulers.blocking import BlockingScheduler


def nowtime1():
    print('time-1: ', time.localtime())


def nowtime2():
    print('time-2: ', time.localtime())


def dingshi3():
    scheduler = BlockingScheduler()
    scheduler.add_job(nowtime1, 'interval', seconds=3, id='job-1')
    scheduler.add_job(nowtime2, 'interval', seconds=1, id='job-2')
    scheduler.start()


from googletrans import Translator


def test():
    source = '挺好'
    # t = json.loads(source)
    # print(t)
    translator = Translator(service_urls=['translate.google.com'])
    text = translator.translate(source, src='zh-cn', dest='en').text
    print(text)


if __name__ == "__main__":
    test()
