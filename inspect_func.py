#coding:utf-8
import time,re
from inspect_words import Kwords
kwords = Kwords()
import inspect_func
import eventlet

def input_select():  #定义需要巡检的主机
    while True:
        inspect_ud = input("是否巡检UD服务器(Y/N):").lower()
        if inspect_ud == "y":
            inspect_ud = True
            break
        elif inspect_ud == "n":
            inspect_ud = False
            break
        else:
            print("请输入y or n !")
    while True:
        inspect_master = input("是否巡检Master服务器(Y/N):").lower()
        if inspect_master == "y":
            inspect_master = True
            break
        elif inspect_master == "n":
            inspect_master = False
            break
        else:
            print("请输入y or n !")
    while True:
        inspect_slaver = input("是否巡检存储服务器(Y/N):").lower()
        if inspect_slaver == "y":
            inspect_slaver = True
            break
        elif inspect_slaver == "n":
            inspect_slaver = False
            break
        else:
            print("请输入y or n !")
    return inspect_ud,inspect_master,inspect_slaver #

def create_slaver_namelist(none_list):
    begin_host = int(input("请输入今天要开始巡检的存储服务器主机名后面数字:"))
    end_host = int(input("请输入今天要结束巡检的存储服务器主机名后面数字:"))
    for host in range(begin_host, end_host + 1):
        host_name = "hadoop-slaver" + str(host)
        none_list.append(host_name)
    # print(none_list)
    return none_list

def create_inspect_dict(inspect_hosts_dict,slaver_list,inspect_ud,inspect_master,inspect_slaver):   #生成一个巡检ip 和主机名对应字典的方法
    with open("ip.txt", "r") as hostfile:
        for line in hostfile.readlines():
            line = line.strip('\n')  # 去掉换行符\n
            b = line.split(' ')  # 将每一行以空格为分隔符转换成列表
            if inspect_ud:
                if b[1] in kwords.ud_lists:
                    inspect_hosts_dict.append(b)
            if inspect_master:
                if b[1] in kwords.master_lists:
                    inspect_hosts_dict.append(b)
            if inspect_slaver:
                if b[1] in slaver_list:
                    inspect_hosts_dict.append(b)
    return dict(inspect_hosts_dict)

#####################################################################################
def get_Host_Name(des_remote,cmd,result_list_info):  #得到主机名，并写入文件
    back_info = des_remote.get_cmd_output(cmd)
    result_list_info.append("主机名:" + back_info + "| ")

def get_Remote_MenInfo(des_remote,cmd,result_list_info): # 得到内存信息，并写入文件
    back_info = des_remote.get_cmd_output(cmd)
    meminfo = float(back_info)
    if meminfo < kwords.MaxValue:
        meminfo = "%.0f%%" % (meminfo * 100)
        result_list_info.append("内存:" + str(meminfo) + "| ")
    else:
        result_list_info.append("内存异常请检查| ")

def get_Remote_CpuInfo(des_remote,cmd,result_list_info): # 得到CPU信息，并写入文件
    back_info = des_remote.get_cmd_output(cmd)
    back_info=float(back_info)
    if back_info < kwords.MaxValue * 100:
        result_list_info.append("CPU使用率:" + str(back_info) + "%| ")
    else:
        result_list_info.append("Cpu异常请检查| ")

def get_Remote_DiskInfo(des_remote,cmd,result_list_info):    #得到硬盘信息并写入文件
    back_info = des_remote.get_cmd_output(cmd)
    back_info = back_info.replace("\r\n", " ")
    use_disk_lists = [i for i in back_info.split(" ")]
    first_disk_use = float(use_disk_lists[0].rstrip("%"))/100
    if first_disk_use < kwords.MaxValue:
        result_list_info.append("存储:" + use_disk_lists[0] + "| ")
    for usedisk in use_disk_lists:
        use = float(usedisk.rstrip("%")) / 100
        if use >= kwords.MaxValue:
            result_list_info.append("存储异常请检查!| ")

def get_Sec(des_remote,cmd,result_list_info):    #得到今天的信安日志快照
    back_info = des_remote.get_cmd_output(cmd)
    back_info = int(back_info)
    if back_info > kwords.NormalValue:
        result_list_info.append("信安日志快照:正常(参考值:" + str(back_info) + ")| ")
    else:
        result_list_info.append("信安日志快照异常 ")

def get_Now_date():   # 得到现在的时间格式 yyyymmdd
    get_time = time.localtime()
    year = str(get_time[0])
    mon = str(get_time[1])
    day = str(get_time[2])

    if len(mon) == 1:
        mon = "0" + mon

    if len(day) == 1:
        day = "0" + day
    now_y_m_d = int(year + mon + day)
    return  now_y_m_d

def check_hadoop_proc(des_remote, cmd ,result_list_info):   # 巡检进程 匹配关键字
    back_info = des_remote.get_cmd_output(cmd)
    fond_kwords_hadoop = re.compile(r"hadoop")
    fond_kwords = fond_kwords_hadoop.search(back_info)
    try:
        result_list_info.append("hadoop进程正常(巡检关键字:"+fond_kwords.group()+")|")
    except AttributeError:
        print("目标主机程序运行异常请检查")

def get_hadoop_use(des_remote, cmd,result_list_info): # 校验master 进程master11-13
    back_info = des_remote.get_cmd_output(cmd)
    result_list_info.append(back_info+" |")

def check_redis(des_remote, cmd ,result_list_info):   #master 14-18 进程
    back_info = des_remote.get_cmd_output(cmd)
    fond_kwords_hadoop = re.compile(r"redis")
    fond_kwords = fond_kwords_hadoop.search(back_info)
    try:
        result_list_info.append("hadoop进程正常(巡检关键字:" + fond_kwords.group() + ")| ")
    except AttributeError:
        print("目标主机程序运行异常请检查")

def check_60001(des_remote ,cmd ,result_list_info):   # 检查60001端口
    back_info = des_remote.get_cmd_output(cmd)
    if int(back_info) > kwords.NormalValue:
        result_list_info.append("60001端口正常| ")
    else:
        result_list_info.append("60001端口异常请查看| ")

def sec_log(des_remote ,cmd ,result_list_info):              #目前的信安日志
    back_info = des_remote.get_cmd_output(cmd)
    result_list_info.append("信安日志:" + back_info + "| ")

def sec_log1(des_remote ,cmd ,result_list_info):             #昨天的信安日志总量
    back_info = des_remote.get_cmd_output(cmd)
    result_list_info.append("信安日志:" + back_info + "| ")

def mate_key(key_str):
    fond_kwords_hadoop = re.compile(r"hadoop-slaver")
    fond_kwords = fond_kwords_hadoop.search(key_str)
    try:
        fond_kwords.group()
    except AttributeError as e:
        return True

def check_datanode_proc(des_remote, cmd ,result_list_info):    # 校验存储服务器进程
    back_info = des_remote.get_cmd_output(cmd)
    fond_kwords_hadoop = re.compile(r"datanode")
    fond_kwords = fond_kwords_hadoop.search(back_info)
    try:
        result_list_info.append("hadoop进程正常(巡检关键字:" + fond_kwords.group() + ")| ")
    except AttributeError:
        result_list_info.append("目标主机程序运行异常请检查| ")
        print("目标主机程序运行异常请检查")

def inspect_ud40(cmd_list,inspect_fun,des_remote ,result_list_info):  # ud40
    for cmd in cmd_list:  # 需要用的命令
        if cmd == cmd_list[0]:  # 主机名
            inspect_func.get_Host_Name(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[1]:  # 内存
            inspect_func.get_Remote_MenInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[2]:  # cpu
            inspect_func.get_Remote_CpuInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[3]:  # 磁盘
            inspect_func.get_Remote_DiskInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[4]:  # 信安日志快照
            inspect_func.get_Sec(des_remote, cmd ,result_list_info)
            
def inspect_ud45_ud46(cmd_list,des_remote ,result_list_info):
    for cmd in cmd_list:  # 需要用的命令
        if cmd == cmd_list[0]:  # 主机名
            inspect_func.get_Host_Name(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[1]:  # 内存
            inspect_func.get_Remote_MenInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[2]:  # cpu
            inspect_func.get_Remote_CpuInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[3]:  # 磁盘
            inspect_func.get_Remote_DiskInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[4]:  # 进程
            inspect_func.check_hadoop_proc(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[5]:  # 60001 端口
            inspect_func.check_60001(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[6]:  # 今天信安日志
            inspect_func.sec_log(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[7]:  # 昨天信安日志快照
            inspect_func.sec_log1(des_remote, cmd ,result_list_info)

def inspect_ud50_ud52(cmd_list,des_remote ,result_list_info):
    for cmd in cmd_list:  # 需要用的命令
        if cmd == cmd_list[0]:  # 主机名
            inspect_func.get_Host_Name(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[1]:  # 内存
            inspect_func.get_Remote_MenInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[2]:  # cpu
            inspect_func.get_Remote_CpuInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[3]:  # 磁盘
            inspect_func.get_Remote_DiskInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[4]:  # 进程
            inspect_func.check_hadoop_proc(des_remote, cmd ,result_list_info)

def inspect_namenode(cmd_list, des_remote ,result_list_info):
    for cmd in cmd_list:
        if cmd == cmd_list[0]:
            inspect_func.get_Host_Name(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[1]:  # 内存
            inspect_func.get_Remote_MenInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[2]:  # cpu
            inspect_func.get_Remote_CpuInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[3]:  # 磁盘
            inspect_func.get_Remote_DiskInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[4]:
            inspect_func.check_hadoop_proc(des_remote, cmd ,result_list_info)

def inspect_redis(cmd_list, des_remote ,result_list_info):
    for cmd in cmd_list:
        if cmd == cmd_list[0]:  # 主机名
            inspect_func.get_Host_Name(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[1]:  # 内存
            inspect_func.get_Remote_MenInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[2]:  # cpu
            inspect_func.get_Remote_CpuInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[3]:  # 磁盘
            inspect_func.get_Remote_DiskInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[4]:  # redis
            inspect_func.check_redis(des_remote, cmd ,result_list_info)
            
def inspect_datanode(cmd_list, des_remote ,result_list_info):
    for cmd in cmd_list:
        if cmd == cmd_list[0]:  # 主机名
            inspect_func.get_Host_Name(des_remote, cmd ,result_list_info)
        if cmd == cmd_list[1]:  # 内存
            inspect_func.get_Remote_MenInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[2]:  # cpu
            inspect_func.get_Remote_CpuInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[3]:  # 磁盘
            inspect_func.get_Remote_DiskInfo(des_remote, cmd ,result_list_info)
        elif cmd == cmd_list[4]:
            inspect_func.check_datanode_proc(des_remote, cmd ,result_list_info)


def RemoteHost_IsActive(jump_server,hostname, username, passwd,set_timeout=kwords.set_timeout):
    eventlet.monkey_patch()
    with eventlet.Timeout(set_timeout, False):
        try:
            des_remote = jump_server.get_remote_session(hostname, username=username, password=passwd,
                                                       retry=0, retry_interval=5)
        except Exception as e :
            print(e)
        des_remote.close()
        return True