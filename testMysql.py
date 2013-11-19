__author__ = 'liuyang'

import MySQLdb

conn=MySQLdb.connect(host="192.168.33.101",user="root", passwd="runstone",db="diboss")

cursor=conn.cursor()

sql="select * from dns_info"

cursor.execute(sql)

results = cursor.fetchall()

print results

conn.close()
