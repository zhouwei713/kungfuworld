'''
Created on 20171208

@author: zhou
'''
'''
get daily sentence and insert to MongoDB
'''

import os, urllib2, urllib, time
from bs4 import BeautifulSoup
from selenium import webdriver
from mongo_conn import Mongo_dailysentence
from date_time import datelist

def dailysentence(date):
    db = Mongo_dailysentence()
    uri = "http://news.iciba.com/views/dailysentence/daily.html#!/detail/title/"
    url = uri + str(date)
    driver = webdriver.PhantomJS(executable_path=r'C:\Users\zhou\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    soup_text = soup.find("div",class_="detail-content-en").text
    soup_img = soup.find("img",class_="detail-banner-img").get('src')
    #here need check whether date in database or not
    rooms = db['dailysentence']
    check_date = rooms.find({"date":date})
    if not check_date or check_date.count() == 0:
        rooms.insert({"date": date, "sentence": soup_text, "picture_url": soup_img})
    print soup_text, soup_img



if __name__ == '__main__':
    DateList = datelist((2017, 1, 3), (2017, 11, 30))
    for i in DateList:
        dailysentence(i)

