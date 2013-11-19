__author__ = 'liuyang'
# -*- coding: utf-8 -*-

import httplib
import time

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

def httpCheckerRun(httpstatsdict):
    myhttpc = httpChecker()
    myhttpc.setup(httpstatsdict)
    while(True):
        myhttpc.check()
        time.sleep(5)

    return

times = 5
passt = 3
initstats = [-1]*times

import copy

class httpChecker:

    #服务器状态，属于全局变量，只有此模块可写，其他模块需要访问该内容
    serverstatus = {}
    #定时检查结果，自有变量，需要结合历史记录最终推导出服务器状态
    servercheckpoints = {}
    #初始阶段不计入状态
    initcount=0


    def setup(self, ssdict):
        self.serverstatus = ssdict
        for key in self.serverstatus.keys():
            self.serverstatus[key] = -1
        self.servercheckpoints = dict((l, copy.copy(initstats)) for l in self.serverstatus.keys())
        self.initcount = 0

    def checkserver(self, url):
        try:
            c = httplib.HTTPConnection(url, timeout=3)
            c.request("HEAD","/")
            s = c.getresponse().status
            #print s
            if(s == 200 or s==304 or s== 302):
                return 1
            return 0
        except:
            return 0

    def check(self):
        if(self.initcount<times):
            self.initcount+=1

        for key in self.serverstatus.keys():
            ret= self.checkserver(key)
            self.servercheckpoints[key].append(ret)
            self.servercheckpoints[key].pop(0)

            if(self.initcount>=times):
                if(sum(self.servercheckpoints[key])>=passt):
                    self.serverstatus[key]=1
                else:
                    self.serverstatus[key]=0

        print self.servercheckpoints
        print self.serverstatus




if __name__ == '__main__':
    #print testResponse("bjdnserror1.wo.com.cn")
    iplist=["202.106.199.34","202.106.199.35","202.106.199.36","202.106.199.37"]
    mdict=dict.fromkeys(iplist,-1)
    print mdict
    httpCheckerRun(mdict)
