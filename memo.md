
开发环境

cd ~/env-py4NDR
source ./bin/activate

退出执行
deactivate

目前已安装的插件有：
?redis
?rq
subprocess32
MySQLdb



在天津管理上已安装redis做为测试，
使用opencsw，注意要修改opencsw的源，版本OK，运行OK
需自行编译redis2.6.13
需自行进行配置文件设定


目前要测试获取系统执行rndc类型的命令时的输出内容，需要考虑超时的问题。

需要将libssl的动态链接库链接到/usr/lib中

