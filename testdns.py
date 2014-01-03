__author__ = 'liuyang'

import subprocess32,shlex


class DnsRDChecker(object):

    rndc = "/usr/local/sbin/rndc"

    def RSreply(self,ip):
        cmd = self.rndc +" -c /Users/liuyang/rs/dns/rndc.conf -s " +ip + " rsia_reply"
        result = self.srun(cmd)

        print result[0]
        print result[1]
        print result[2]
        #rndcPOpen=subprocess32.Popen(args=cmd, stdout=subprocess32.PIPE, stderr=subprocess32.PIPE)

        #print rndcPOpen.stdout.read()
        #print rndcPOpen.stderr.read()

    def test(self):
        try:
            cmd = "uptime"
            r = subprocess32.Popen(args=cmd, shell=True, stdout=subprocess32.PIPE, stderr=subprocess32.PIPE)
            #r.wait(timeout=3)
            print r.stderr.read()
            print r.stdout.read()
        except:
            print r.stderr.read()
            print r.stdout.read()

    def test2(self):
        try:
            cmd = "/sbin/ping -c 5 192.168.1.1"
            r = subprocess32.Popen(shlex.split(cmd),stdout=subprocess32.PIPE, stderr=subprocess32.PIPE)
            #stdout, stderr = r.communicate(timeout=3)
            stdout, stderr = r.communicate(timeout=3)
            print stdout
            print stderr
        except subprocess32.TimeoutExpired:
            r.kill()
            stdout, stderr = r.communicate()
            print stdout
            print stderr

    def srun(self,cmd, otime=3):
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

    def test3(self):
        with subprocess32.Popen(["iostat","1"], stdout=subprocess32.PIPE) as proc:
            print proc.stdout.read()


if __name__ == '__main__':
    d = DnsRDChecker()
    #d.test2()
    d.RSreply("192.168.33.101")
    d.RSreply("123.124.198.61")

