# jumpremote

  
## 说明：
```bash
    此程序基于Python jumpssh库开发，jumpssh是基于paramiko的高级封装，更加易于使用，paramiko 使用比较复杂。该程序在Python3.x环境下运行，
在windows环境下开发。可用通过跳板机到目标服务器的巡检。自动采集内存、CPU、硬盘使用情况业务进程等信息，生成日志；不会写多线程是此程序的缺点，
应该还有地方有bug比如时间在每个月1日会报错，之后会慢慢修改。
```
<br>
<br>

- 1、main_auto_inspect  主程序，程序运行的逻辑关系大多在此。
- 2、inspect_fun        主程序封装的函数。
- 3、inspect_cmd        采集服务器信息需要的命令，在一个列表里面。
- 4、inspect_words      存放用户名跳板机等参数，已经在文件里面备注。
- 5、ip.txt             存放ip和主机名的对应关系，传入新的主机需按照里面的格式一致，通过函数方法生成采集主机的ip和主机名对应的字典。
- 6、inspect_log.log    采集主机信息之后产生的日志，用于主机资源使用率的分析。

# 后记

> 2024年12月17日,这个程序是在刚出来实习的时候写的那个时候实习在数据中心巡检每天都是重复的工作再加上那时候时间充裕便自学python,这个是第一个用于减少自己工作量的程序，真是技术改变自己啊，那个时候一个小时的工作在自动化之后10分钟内便可以完成。那个时候真引以为傲啊，在公司的老员工都有些许赞。
> 
> 那个时候还是2019年，那个时候还没有疫情. 时间过的真快啊转眼已经5年过去了，五年中也在不断的学习和积累，蓦然回首再回来看这段代码，有了更多的见解，感触颇多。
> 
> 现在看来这个项目太low了准备弃用,留作纪念放在仓库。
> 
> 2024年12月17日
