#!/usr/bin/python3
# -*- coding: utf8 -*-
# author: s1g0day
# update: 2025-03-11 11:42

import sys
import warnings
import importlib
from io import StringIO
from lib.logo import logo
from lib.notify import send
warnings.filterwarnings("ignore")

def sign_main():
    logo()
    # 定义每个文件的模块名和主函数名
    file_data = [
        {"title": f"{'#' * 20}运行服务器{'#' * 20}","module_name": "lib.get_public_ip", "main_function": "get_public_ip_main"},
        {"title": "🔞 续费通知 🔞","module_name": "modules.renew.renew", "main_function": "renew_main"},
        {"title": " t00ls 签到通知", "module_name": "modules.t00ls.t00ls", "main_function": "t00ls_main"},
        {"title": " threatbook 签到通知", "module_name": "modules.threatbook.threatbook", "main_function": "threatbook_main"},
        # {"title": " ruike 签到通知","module_name": "modules.discuz.discuz-nocode-ruike", "main_function": "discuz_ruike_main"},
        # {"title": " hostloc 签到通知","module_name": "modules.discuz.discuz-nocode-hostloc", "main_function": "discuz_hostloc_main"},
        {"title": "🐟🐟🐟 摸鱼提醒 🐟🐟🐟", "module_name": "modules.fishing.fish_reminder", "main_function": "fishReminder_main"},
    ]

    # 运行每个文件并获取打印的内容
    for data in file_data:
        module_name = data["module_name"]
        main_function = data["main_function"]
        # 重定向stdout到一个StringIO对象
        stdout_backup = sys.stdout
        sys.stdout = StringIO()
        module = importlib.import_module(module_name)
        result = getattr(module, main_function)()  # 调用每个文件的主函数
        # 获取打印的内容
        output = sys.stdout.getvalue()
        # 还原stdout
        sys.stdout = stdout_backup
        if output:
            send(data["title"],output)
    return "success"

if __name__ == "__main__":
    sign_main()