import jumpssh
import inspect_func

nowdate  = inspect_func.get_Now_date()

class InspectCmd():
    def __init__(self):
        self.cmd_lists=[
                        """hostname""",
                        """ps -ef | grep java""",
                        """netstat -an|grep -c 60001""",
                        """wc -l /home/ud/udxdr/backup/$(date '+%Y%m%d')/* |tail -n 1 | awk '{print $1}'""",
                        """wc -l /home/ud/udxdr/backup/$(date '+%Y%m%d' -d -1day)/* |tail -n 1 | awk '{print $1}'""",
                        r"""find /home/ud/html-snapshot/snapshot/$(date +%Y%m%d)/ -mmin -5|wc -l""",

                        """hdfs dfs -df -h | grep hdfs | awk '{print $8}' """,
                        """ps -ef | grep hadoop""",
                        """ps -ef ｜　grep redis""",
                        """ps -ef | grep datanode""",

                        r"""mt=`grep 'MemTotal:' /proc/meminfo |awk '{print $2}'`;ma=`grep 'Active:' /proc/meminfo|awk '{print $2}'`;mf=`expr $mt - $ma`;echo 'Memory:' `expr $mt / 1024`'M' all `expr $mf / 1024`'M' avail | awk  '{print ($2-$4)/$2}'""",
                        r"""sar -u 1 2 | sed '/^$/d' | awk '{print $3}' | tail -n 1 """,
                        """df -h|awk 'NR!=1{if ( NF == 6 ) {print $5} else if ( NF == 5) {print $4} }'  """,
                        ]

# print(help(jumpssh))