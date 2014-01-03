__author__ = 'liuyang'
# -*- coding: utf-8 -*-

import httplib
import time


def httpCheckerRun(httpstatsdict, ipmap, interval):
    myhttpc = httpChecker()
    myhttpc.setup(httpstatsdict, ipmap)
    while(True):
        myhttpc.check()

        print httpstatsdict

        time.sleep(interval)

    return

#一个检查周期设为5次
times = 5
#这5次中状态OK的次数超过3次被视为服务器状态正常
passt = 3
#这是初始化一个周期内状态的初值常量
initstats = [-1]*times

import copy

class httpChecker:

    #服务器状态，属于全局变量，只有此模块可写，其他模块需要访问该内容
    serverstatus = {}
    #定时检查结果，自有变量，需要结合历史记录最终推导出服务器状态
    servercheckpoints = {}
    #初始阶段不计入状态
    initcount=0
    #公网和内网IP地址映射表
    ipmap = ()

    def setup(self, ssdict, ipmap):
        self.serverstatus = ssdict
        self.ipmap = ipmap
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
            if(s == 200 or s==304 or s== 302 or s==301):
                return 1
            return 0
        except:
            return 0

    def check(self):
        if(self.initcount<times):
            self.initcount+=1

        for key in self.serverstatus.keys():
            checkip = self.ipmap[key]
            ret = (self.checkserver(checkip) and self.checkserver(checkip+":8080"))
            self.servercheckpoints[key].append(ret)
            self.servercheckpoints[key].pop(0)

            if(self.initcount>=times):
                if(sum(self.servercheckpoints[key])>=passt):
                    self.serverstatus[key]=1
                else:
                    self.serverstatus[key]=0

        #print self.servercheckpoints
        #print self.serverstatus

import threading

class httpCheckerThread(threading.Thread):
    #初始化参数，网站ip地址对（公网：内网），网站ip对应状态（公网:状态），检查间隔（秒）
    def __init__(self, ipmap, httpstatsdict, ss=5):
        self.ss = int(ss)
        self.ipmap = ipmap
        self.httpstatsdict = httpstatsdict
        self.keepRunning = 1
        threading.Thread.__init__(self)

    def run(self):
        myhttpc = httpChecker()
        myhttpc.setup(self.httpstatsdict, self.ipmap)
        while(self.keepRunning):
            myhttpc.check()
            #print httpstatsdict
            time.sleep(self.ss)

    def stop(self):
        self.keepRunning = 0;

if __name__ == '__main__':
    #print testResponse("bjdnserror1.wo.com.cn")
    iplist=["202.106.199.34","202.106.199.35","202.106.199.36","202.106.199.37","123.129.254.14"]
    interip = ["202.106.199.34","202.106.199.35","202.106.199.36","202.106.199.37","123.129.254.14"]
    mdict=dict.fromkeys(iplist,-1)
    ipmap = dict(zip(iplist, interip))

    print mdict
    print ipmap

    httpCheckerRun(mdict, ipmap, 6)
