#!/usr/bin/python3
# -*- coding: utf8 -*-


import sys
import warnings
import importlib
from io import StringIO
from lib.notify import send
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    
    # 定义每个文件的模块名和主函数名
    file_data = [
        {'title': '🔞 续费通知','module_name': 'modules.renew.renew', 'main_function': 'renew_main'},
        {'title': '🔞 t00ls 签到通知', 'module_name': 'modules.t00ls.t00ls', 'main_function': 't00ls_main'},
        {'title': '🔞 hostloc 签到通知','module_name': 'modules.discuz.discuz-nocode-v2', 'main_function': 'discuz_main'},
    ]

    # 运行每个文件并获取打印的内容
    for data in file_data:
        module_name = data['module_name']
        main_function = data['main_function']
        # 重定向stdout到一个StringIO对象
        stdout_backup = sys.stdout
        sys.stdout = StringIO()

        module = importlib.import_module(module_name)
        result = getattr(module, main_function)()  # 调用每个文件的主函数
        # 获取打印的内容
        output = sys.stdout.getvalue()
        # 还原stdout
        sys.stdout = stdout_backup
        # print("params",output)
        if output:
            send(data['title'],output)
        