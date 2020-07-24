
class Kwords():
    def __init__(self):
        self.MaxValue=0.9       #cpu阈值大于90%，日志显示不正常
        self.NormalValue=100     #60001端口数量大于100
        self.set_timeout=4          #链接目标主机超时4s
        self.jump_HostIp=""        #跳板机 IP
        self.jump_HostPort=""               #跳板机端口
        self.jump_HostUser=''                #跳板机用户名
        self.jump_HostPass=''        #跳板机密码
        self.des_Ud_HostUser=""               #目标主机用户名
        self.des_Ud_HostPass=''
        self.des_master_user="hado"           #目标主机用户名
        self.des_master_pass='cQIsm#'
        self.curre_username = "hado"
        self.ud_lists = ['cu-ud40','cu-ud45','cu-ud46','cu-ud50','cu-ud51','cu-ud52']
        self.master_lists = ["hadoop-master11","hadoop-master12","hadoop-master13",
                             "hadoop-master14","hadoop-master16","hadoop-master17",
                             "hadoop-master18"]
