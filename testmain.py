__author__ = 'liuyang'
# -*- coding: utf-8 -*-

import getopt
import sys,time
import threading

import config
import dnsInfo
import dnsMonitor
import httpMonitor
import rsRndc
import dnsAdjustment

def usage():
    print "usage:[options]"
    print "options:"
    #print ""
    print "-h, --help show this help message and exit"
    print "-cFile --config=File File is config file"


def main(argv):
    ######################
    #read config file
    ######################
    configfile = "config.ini"
    try:
        opts, args = getopt.getopt(argv, "hc:",["help", "config="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--config"):
            configfile = arg


    gv = config.globalValues()
    gv.Config(configfile)
#    attrs = vars(gv)
#    print ",  ".join("%s: %s" %item for item in attrs.items())

    #######################
    # get dns list
    #######################
    mydns = dnsInfo.Dns()
    mydns.setDB(gv.db_host, gv.db_user, gv.db_passwd, gv.db_port, gv.db_name)
    mydns.refreshList()

    dnslist = mydns.getDnsList()

    ########################
    # init checking dns state
    ########################
    dnsstats={}
    for dnsip in dnslist:
        dnsstats[dnsip] = [-1,[]]

#    dnsthread = threading.Thread(target=dnsMonitor.dnsCheckRun,args=(dnsstats,))
#    dnsthread.start()
    #mrndc = rsRndc.rsRndc(rndc="/usr/local/sbin/rndc",conf="/Users/liuyang/rs/dns/rndc.conf")
    mrndc = rsRndc.rsRndc(rndc=gv.bind_rndc, conf=gv.bind_conf)
    dnsthread = dnsMonitor.dnsCheckThread(dnsstats, mrndc, gv.dns_check_interval)
    dnsthread.start()

    #dnsMonitor.dnsCheckRun(dnsstats)

    ########################
    # init checking http state
    ########################
    mdict=dict.fromkeys(gv.ipList,-1)

#    httpthread=threading.Thread(target=httpMonitor.httpCheckerRun,args=(mdict,))
#    httpthread.start()

    httpthread = httpMonitor.httpCheckerThread(gv.ipdict, mdict, gv.web_check_interval)
    httpthread.start()

    dnsad = dnsAdjustment.dnsRsAdjustment(mrndc)
    try:
        while True:
            print dnsstats
            print mdict
            #如果http中可用的服务器诶有了，就不要做任何调整了
            httponlines,httpofflines = dnsad.dnsAdjustment(dnsstats,mdict)
            if(len(httponlines)>0 and len(httpofflines)>0):
                mydns.updatefactor(httponlines[0],httpofflines)

            #需要调整数据库中的信息。

            time.sleep(int(gv.adjust_interval))
    except:
        dnsthread.join()
        httpthread.join()
    #httpMonitor.httpCheckerRun(mdict)


if __name__ == "__main__":
    main(sys.argv[1:])