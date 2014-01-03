__author__ = 'liuyang'
import MySQLdb


class Dns(object):

    DnsList=[]

#    def __init__(self):

    def setDB(self, dbhost, dbuser, passwd, port, dbname):
        self.dbhost = dbhost
        self.dbuser = dbuser
        self.passwd = passwd
        self.port = port
        self.dbname = dbname

    def refreshList(self):
        ret = 1
        conn=MySQLdb.connect(host=self.dbhost,user=self.dbuser, passwd=self.passwd,
                             port=self.port, db=self.dbname)

        cursor=conn.cursor()

        sql="select dns_ip from dns_info where dns_status=1"

        cursor.execute(sql)

        results = cursor.fetchall()

        if not results:
            ret = 0
        else:
            self.DnsList=[]
            for row in results:
                self.DnsList.append(row[0])

        conn.close()
        return ret

    def getDnsList(self):
        return self.DnsList

    def updatefactor(self, onlineIP, offlineIPs):
        if(len(offlineIPs) == 0):
            return

        conn=MySQLdb.connect(host=self.dbhost,user=self.dbuser, passwd=self.passwd,
            port=self.port, db=self.dbname)
        wherein="(%s)"
        format_string=','.join(['%s'] * len(offlineIPs))
        wherein = wherein % format_string

        cursor=conn.cursor()
        sql="update factor_info set factor_ip = %s where factor_ip in " + wherein

        v = [onlineIP]+offlineIPs
        cursor.execute(sql,v)

        conn.commit()
        conn.close()

        return

if __name__ == '__main__':
    import config
    gv = config.globalValues()
    gv.Config("config.ini")

#    attrs = vars(gv)
#   print ",  ".join("%s: %s" %item for item in attrs.items())

    mydns=Dns()
#    mydns.setDB("192.168.33.101","root", "runstone", 3306, "diboss")
    mydns.setDB(gv.db_host, gv.db_user, gv.db_passwd, gv.db_port, gv.db_name)
    mydns.refreshList()
    print mydns.getDnsList()

    mydns.updatefactor("202.106.199.33",["202.106.199.35","202.106.199.38"])
    mydns.updatefactor("202.106.199.35",["202.106.199.39"])