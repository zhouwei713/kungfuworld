'''
Created on 20171117

@author: zhou
'''

import urllib, urllib2, sys, json

def todayonhistory(m, d):
    uri = "http://history.muffinlabs.com/date/"
    month = str(m)
    day = str(d)
    url = uri + month + "/" + day
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    content = resp.read()
    r = json.loads(content)
    return r['data']
#     print r['data']['Events'][0]
#
# if __name__=='__main__':
#     todayonhistory(11,11)
