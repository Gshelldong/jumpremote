# jumpremote

  
## 说明：
    此程序基于Python jumpssh库开发，jumpssh是基于paramiko的高级封装，更加易于使用，paramiko 使用比较复杂。该程序在Python3.x环境下运行，
在windows环境下开发。可用通过跳板机到目标服务器的巡检。自动采集内存、CPU、硬盘使用情况进程等信息，生成日志；不会写多线程是此程序的缺点，
应该还有地方有bug比如时间在每个月1日会报错，之后会慢慢修改。

<br>
<br>

- 1、main_auto_inspect  主程序，程序运行的逻辑关系大多在此。
- 2、inspect_fun        主程序封装的函数。
- 3、inspect_cmd        巡检服务器需要的命令，在一个列表里面。
- 4、inspect_words      存放用户名跳板机等参数，已经在文件里面备注。
- 5、ip.txt             存放ip和主机名的对应关系，传入新的主机需按照里面的格式一致，通过函数方法生成巡检ip和主机名对应的字典。
- 6、inspect_log.log    巡检主机之后产生的日志，用于每日作业计划的分析。
