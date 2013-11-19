__author__ = 'liuyang'
# -*- coding: utf-8 -*-

import subprocess32,shlex
import time

def dnsCheckRun(dnsStatsDict):
    mydnsChecker=dnsChecker(rndc="/usr/local/sbin/rndc",conf="/Users/liuyang/rs/dns/rndc.conf")
    mydnsChecker.setup(dnsStatsDict)
    while(True):
        mydnsChecker.check()
        print dnsStatsDict
        time.sleep(5)



class dnsChecker:
    #全局的dns状态信息，由外部传入
    dnsstats = {}
    rndc = '/sbin/rndc'
    conf = '/etc/rndc.conf'
    timeout = 3

    def __init__(self, **kwargs):
        if kwargs.has_key('rndc'):
            self.rndc = kwargs['rndc']
        if kwargs.has_key('conf'):
            self.conf = kwargs['conf']
        if kwargs.has_key('timeout'):
            self.timeout = kwargs['timeout']


    def setup(self, gdnsstats):
        self.dnsstats=gdnsstats


    def check(self):
        for dnsip in self.dnsstats.keys():
            self.checkreply(dnsip)
        return

    def checkreply(self, dnsip):
        cmd = self.rndc + " -c " + self.conf + " -s " + dnsip + " rsia_reply"
        result = self.srun(cmd, self.timeout)
        if(result[0] == 0):
            #得到dns上的ip转发列表
            self.dnsstats[dnsip][0]=1
            self.dnsstats[dnsip][1]=result[1].strip().split("\n")
        else:
            #访问dns出错
            self.dnsstats[dnsip][0]=0
            self.dnsstats[dnsip][1]=[]

        return


    def srun(self, cmd, otime):
        try:
            r = subprocess32.Popen(shlex.split(cmd),stdout=subprocess32.PIPE, stderr=subprocess32.PIPE)
            stdout, stderr = r.communicate(timeout=otime)
            ret = r.returncode
            #print stdout
            #print stderr
            return [ret, stdout, stderr]
        except subprocess32.TimeoutExpired:
            r.kill()
            stdout, stderr = r.communicate()
            #print stdout
            #print stderr
            return [1, stdout, stderr]


if __name__ == '__main__':
    dnsstats={}
    dnsstats["192.168.33.101"]=[0,[]]
    dnsstats["123.124.198.61"]=[0,[]]
    dnsCheckRun(dnsstats)
