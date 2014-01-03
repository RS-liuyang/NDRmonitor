__author__ = 'liuyang'

import subprocess32
#import multiprocessing.dummy as multiprocessing
subprocess=subprocess32

def fun(cmd):
    try:
        #cmd = "ping 192.168.1.1"
        r = subprocess.Popen(args=cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdout, stderr = r.communicate(timeout=3)
        stdout, stderr = r.communicate(timeout=3)

        print stdout
        print stderr
        return True
    except subprocess.TimeoutExpired:
        r.kill()
        stdout, stderr = r.communicate()
        print stdout
        print stderr
        return False

def fun2():
    try:
        r = subprocess.Popen(['/usr/bin/dig', ' @192.168.1.1', ' runstone.com'],
                             shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdout, stderr = r.communicate(timeout=3)
        (stdoutdata,stderrdata)=r.communicate(timeout=3)
        #if r.stdout:
        #print r.stdout.read()
        print stdoutdata
        print r.stderr.read()
        #print r.stderrdata
    except subprocess.TimeoutExpired:
        r.kill()
        stdout, stderr = r.communicate()
        print stdout
        print stderr

if __name__ == '__main__':
    print fun("dig @192.168.1.1 www.runstone.com")
    print fun("iostat 1")
    #print fun2()