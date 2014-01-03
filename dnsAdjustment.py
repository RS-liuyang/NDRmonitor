__author__ = 'liuyang'
# -*- coding: utf-8 -*-

import rsRndc

#如果httpstats中的ip状态是-1，那么dnsstats中的有这个IP，则不作删除操作，如果没有这个IP，则不做增加操作
#

class dnsRsAdjustment():

    def __init__(self, rsRndc):
        self.rsrndc = rsRndc

    def dnsAdjustment(self, dnsstats, httpstats):

        #httpstats状态为-1和1的列表，做删除计算的时候使用，如果dns上的ip地址不属于该列表，则需要删除
        httpiplist1=[]
        httpiplist2=[]
        httpofflineiplist=[]
        for httpip, httpstat in httpstats.iteritems():
            if httpstat == 1:
                httpiplist1.append(httpip)
                httpiplist2.append(httpip)
            if httpstat == -1:
                httpiplist1.append(httpip)
            if httpstat == 0:
                httpofflineiplist.append(httpip)

        #可用http列表为空，则不作修改，直接返回
        if(len(httpiplist2) < 1):
            return httpiplist2, httpofflineiplist
        #httpstats状态为1的列表，做增加操作，如果该列表中的IP没有出现在dns中，则需要增加。

        for dnsip, dnsstat in dnsstats.iteritems():
            dnss = dnsstat[0]

            if(dnss != 1):
                continue

            dnsrset = set(dnsstat[1])

            dnsset1 = set(httpiplist1)
            dnsset2 = set(httpiplist2)

            dns2add = list(dnsset2.difference(dnsrset))
            dns2del = list(dnsrset.difference(dnsset1))
            #print dnsrset
            #print dnsset1
            #print dns2add
            #print dns2del


            self.dnsadjusting(dnsip, dns2add, dns2del)

        return httpiplist2, httpofflineiplist

    def dnsadjusting(self, dnsip, addlist, dellist):

        for ip in addlist:
            self.rsrndc.addip(dnsip, ip)
        for ip in dellist:
            self.rsrndc.delip(dnsip, ip)


if __name__ == '__main__':
    myrndc = rsRndc.rsRndc(rndc="/usr/local/sbin/rndc",conf="/Users/liuyang/rs/dns/rndc.conf")
    mydra = dnsRsAdjustment(myrndc)
    dnsstats={"192.168.33.101":[1,["192.168.33.201","192.168.33.202", "192.168.33.203", "192.168.33.204"]]}
    httpstats={"192.168.33.201":1, "192.168.33.202":0,"192.168.33.203":1, "192.168.33.204":0}
    mydra.dnsAdjustment(dnsstats, httpstats)
