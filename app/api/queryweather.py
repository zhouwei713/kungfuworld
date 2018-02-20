'''
Created on 20171119

@author: zhou
'''



import json, urllib2, urllib, os, sys

def queryweather(city):
    uri = "https://way.jd.com/he/freeweather?city="
    ct = city
    url = uri + ct + "&appkey=5811017734c5b78c82804af99c241e05"
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    content = resp.read()
    r = json.loads(content)
    print r['msg']

# if __name__=='__main__':
#     queryweather('beijing')