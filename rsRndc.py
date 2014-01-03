__author__ = 'liuyang'
# -*- coding: utf-8 -*-

import subprocess32,shlex

class rsRndc():
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

    def srun(self, cmd, otime):
        try:
            r = subprocess32.Popen(shlex.split(cmd),stdout=subprocess32.PIPE, stderr=subprocess32.PIPE)
            stdout, stderr = r.communicate(timeout=otime)
            ret = r.returncode
            return [ret, stdout, stderr]

        except subprocess32.TimeoutExpired:
            r.kill()
            stdout, stderr = r.communicate()
            return [1, stdout, stderr]

    def checkreply(self, dnsip):
        cmd = self.rndc + " -c " + self.conf + " -s " + dnsip + " rsia_reply"
        return self.srun(cmd, self.timeout)

    def addip(self, dnsip, httpip):
        cmd = self.rndc + " -c " + self.conf + " -s " + dnsip + " rsia_start " + httpip + " 1"
        return self.srun(cmd, self.timeout)

    def delip(self, dnsip, httpip):
        cmd = self.rndc + " -c " + self.conf + " -s " + dnsip + " rsia_stop " + httpip
        return self.srun(cmd, self.timeout)


if __name__ == '__main__':
    myrndc = rsRndc(rndc="/usr/local/sbin/rndc",conf="/Users/liuyang/rs/dns/rndc.conf")
    print myrndc.checkreply("192.168.33.101")
    print myrndc.addip("192.168.33.101", "192.168.33.201")
    print myrndc.addip("192.168.33.101", "192.168.33.202")
    print myrndc.addip("192.168.33.101", "192.168.33.203")
    print myrndc.addip("192.168.33.101", "192.168.33.204")
    print myrndc.checkreply("192.168.33.101")

'''
    print myrndc.delip("192.168.33.101", "192.168.33.201")
    print myrndc.delip("192.168.33.101", "192.168.33.202")
    print myrndc.checkreply("192.168.33.101")
'''