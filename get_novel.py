# coding = utf-8
"""
@author: zhou
@time:2019/3/21 18:27
"""


import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import json
import time
import os


def save_to_csv(novel_name, chapter, details):
    print('save to txt')
    os.chdir(r'file')
    if not os.path.exists(novel_name):
        os.makedirs(novel_name)
    os.chdir(novel_name)
    with open(chapter[0] + chapter[1] + '.txt', 'w', encoding='gb18030') as f:
        for i in range(len(details)):
            s = details[i] + '\n'
            f.write(s)
    print('save finish!')


def get_chapter_feihuwaizhuan():
    url = 'http://www.jinyongwang.com/fei'
    res = requests.get(url).text
    content = BeautifulSoup(res, "html.parser")
    ul = content.find('ul', attrs={'class': 'mlist'}).find_all('li')
    chapter = []
    for i in ul:
        chap_name = i.find('a').text.split('\u3000')
        # print(chap_name)
        if len(chap_name) == 2:
            chap = chap_name[0]
            name = chap_name[1]
            uri = i.find('a')['href']
            # print(chap_name, uri)
            chapter.append([chap, name, uri])
    return chapter


def get_detail_feihuwaizhuan():
    baseurl = 'http://www.jinyongwang.com'
    chapter = get_chapter_feihuwaizhuan()
    text_list = []
    for i in chapter:
        print(i)
        url = baseurl + i[2]
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        div = content.find('div', attrs={'class': 'vcon'}).find_all('p')
        details = []
        for p in div:
            de = p.text
            details.append(de)
        print(details)
        save_to_csv('飞狐外传', i, details)
        translator = Translator(service_urls=['translate.google.com'])
        chap = translator.translate(i[0], src='zh-cn', dest='en').text
        name = translator.translate(i[1], src='zh-cn', dest='en').text
        tmp = []
        for t in details:
            text = translator.translate(t, src='zh-cn', dest='en').text
            tmp.append(text)
        text_list.append([chap, name, tmp])
        print(text_list)
        # break
        print(time.localtime())
        public_feihuwaizhuan(text_list)
        time.sleep(300)  # 暂停一小时
    return text_list


def public_feihuwaizhuan(text):
    # text = get_detail_feihuwaizhuan()
    url = 'http://127.0.0.1:9980/publish/api/post'
    headers = {
        'Content-Type': "application/json"}
    data = {
    "name": "Flying fox",
    "chapter": text[0][0],
    "postname": text[0][1],
    "postbody": text[0][2],
    "tag": "wuxia",
    "original": "Jin Yong",
    "picture": "/static/post/images/jinyong01.jpg",
    "author_id": 1,
    "key": "hard to guess"
}
    res = requests.post(url, data=json.dumps(data), headers=headers)
    return res.text


if __name__ == "__main__":
    get_detail_feihuwaizhuan()
    # public_feihuwaizhuan()
