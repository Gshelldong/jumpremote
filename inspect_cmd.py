import jumpssh
import inspect_func

nowdate  = inspect_func.get_Now_date()

class InspectCmd():
    """
    这个类定义了巡检的命令.
    """
    def __init__(self):
        self.cmd_lists=[
                        """hostname""",
                        """ps -ef | grep java"""
                        ]