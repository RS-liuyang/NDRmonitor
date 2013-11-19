__author__ = 'liuyang'
import copy

list=[1,2,3,4,5]

ik=[-1]*5

d1 = dict.fromkeys(list, copy.copy([0,0,0,0,0]))

d2 = dict((i, copy.copy(ik)) for i in list)

d1[1].append(2)

d2[1].append(2)

print d1
print d2
