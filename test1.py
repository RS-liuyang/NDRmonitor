__author__ = 'liuyang'

import httplib
import urllib2

def testResponse(url):
    try:
        c = httplib.HTTPConnection(url, timeout=3)
        c.request("HEAD","/")
        s = c.getresponse().status
        #print s
        if(s == 200 or s==304 or s== 302):
            return True
        return False
    except:
        return False

def testResponse2(url):
    try:
        data=urllib2.urlopen("http://"+url, timeout=3).read()
        print data
        return True
    except:
        return False

print testResponse("nmgdnserror1.wo.com.cn")
print testResponse("bjdnserror1.wo.com.cn")
print testResponse("bjdnserror2.wo.com.cn")

print testResponse2("bjdnserror2.wo.com.cn")