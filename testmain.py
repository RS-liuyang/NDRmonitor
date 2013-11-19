__author__ = 'liuyang'

import getopt
import sys

import config
import dnsInfo
import dnsMonitor
import httpMonitor


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
    # check dns state
    ########################
    dnsstats={}
    for dnsip in dnslist:
        dnsstats[dnsip] = [-1,[]]
    #dnsMonitor.dnsCheckRun(dnsstats)

    ########################
    # check http state
    ########################
    mdict=dict.fromkeys(gv.ipList,-1)
    httpMonitor.httpCheckerRun(mdict)



if __name__ == "__main__":
    main(sys.argv[1:])