'''
Created on 20171119

@autho
'''

#encoding: utf-8

import urllib, urllib2, json

def talkrobot(info):
    uri = "https://way.jd.com/turing/turing?info="
    info1 = info
    userid = 222
    url = uri + info1 + "&loc=beijing" + "userid=222" + "&appkey=5811017734c5b78c82804af99c241e05"
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    content = resp.read()
    #print content
    r = json.loads(content)
    if r['result']['code'] == 302000:
        return r['result']['list'][0]['detailurl']
    elif r['result'].has_key('url'):
        return r['result']['url']
    else:
        return r['result']['text']

# if __name__=='__main__':
#      s = "News"
#      talkrobot(s)
#     #print s


