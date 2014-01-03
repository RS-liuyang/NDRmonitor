__author__ = 'liuyang'
# -*- coding: utf-8 -*-

import subprocess32,shlex
import time
import rsRndc

def dnsCheckRun(dnsStatsDict):
    mrndc = rsRndc.rsRndc(rndc="/usr/local/sbin/rndc",conf="/Users/liuyang/rs/dns/rndc.conf")
    mydnsChecker=dnsChecker(mrndc)
    mydnsChecker.setup(dnsStatsDict)
    while(True):
        mydnsChecker.check()
        print dnsStatsDict
        time.sleep(5)



class dnsChecker:
    #全局的dns状态信息，由外部传入
    dnsstats = {}

    def __init__(self, rsRndc):
        self.rsrndc = rsRndc


    def setup(self, gdnsstats):
        self.dnsstats=gdnsstats


    def check(self):
        for dnsip in self.dnsstats.keys():
            self.checkreply(dnsip)
        return

    def checkreply(self, dnsip):
        result = self.rsrndc.checkreply(dnsip)
        if(result[0] == 0):
            #得到dns上的ip转发列表
            self.dnsstats[dnsip][0]=1
            self.dnsstats[dnsip][1]=result[1].strip().split("\n")
        else:
            #访问dns出错
            self.dnsstats[dnsip][0]=0
            self.dnsstats[dnsip][1]=[]

        return

import threading
class dnsCheckThread(threading.Thread):
    def __init__(self, dnsStatsDict, rsRndc, ss=5):
        self.dnsStatsDict = dnsStatsDict
        self.ss = int(ss)
        self.rsrndc = rsRndc
        self.keepRunning = 1
        threading.Thread.__init__(self)

    def run(self):
        mydnsChecker = dnsChecker(self.rsrndc)
        mydnsChecker.setup(self.dnsStatsDict)
        while(self.keepRunning):
            mydnsChecker.check()
            #print httpstatsdict
            time.sleep(self.ss)

    def stop(self):
        self.keepRunning = 0;

if __name__ == '__main__':
    dnsstats={}
    dnsstats["192.168.33.101"]=[0,[]]
    dnsstats["123.124.198.61"]=[0,[]]
    dnsCheckRun(dnsstats)
