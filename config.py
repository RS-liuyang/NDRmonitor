__author__ = 'liuyang'

import ConfigParser

class globalValues(object):
    db_host=""
    db_user=""
    db_passwd=""
    db_port=3306
    db_name="diboss"

    ipList=[]
    internal_ipList=[]
    ipdict={}

    bind_rndc="/sbin/rndc"
    bind_conf="/etc/rndc.conf"

    dns_check_interval=300
    web_check_interval=300
    adjust_interval=3600

    def Config(self, configFile):
        cf = ConfigParser.ConfigParser()
        cf.read(configFile)

        self.db_host=cf.get("db","host")
        self.db_user=cf.get("db","user")
        self.db_passwd=cf.get("db", "passwd")
        self.db_port = cf.getint("db", "port")
        self.db_name = cf.get("db", "db")

        self.ipList=cf.get("web","ip").split(",")
        self.internal_ipList=cf.get("web", "internal-ip").split(",")
        self.ipdict = dict(zip(self.ipList, self.internal_ipList))

        self.bind_rndc=cf.get("bind", "rndc")
        self.bind_conf=cf.get("bind", "conf")

        self.dns_check_interval = cf.get("monitor", "dns-check-interval")
        self.web_check_interval = cf.get("monitor", "web-check-interval")
        self.adjust_interval = cf.get("monitor", "adjust-interval")

        return

def getConfig(configFile, gv):
    cf = ConfigParser.ConfigParser()
    cf.read(configFile)

    gv.db_host=cf.get("db","host")
    gv.db_user=cf.get("db","user")
    gv.db_password=cf.get("db", "passwd")
    gv.db_port = cf.getint("db", "port")
    gv.db_name = cf.get("db", "db")

    gv.ipList=cf.get("web","ip").split(",")


    return

if __name__ == '__main__':
    gv = globalValues()
    gv.Config("config.ini")
    attrs = vars(gv)

    print ",  ".join("%s: %s" %item for item in attrs.items())