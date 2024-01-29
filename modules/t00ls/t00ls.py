# -*- coding: utf-8 -*-

import yaml
import time
from datetime import datetime
from modules.t00ls.src.tslogin import tslogin
from modules.t00ls.src.tsignin import tsignin
from modules.t00ls.src.tsactivity import tsactivity_main
from modules.t00ls.src.domain_query import domain_name_query

def t00ls_main():
    # 加载配置
    push_config = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8").read())

    login_list = []
    for key in push_config:
        if key.startswith('t00ls_username'):
            index = key.split('t00ls_username')[1]
            domain = push_config['t00ls_domain']
            username = push_config['t00ls_username' + index]
            password = push_config['t00ls_password' + index]
            qesnum = push_config['t00ls_qesnum' + index]
            qan = push_config['t00ls_qan' + index]
            login_list.append({
                't00ls_domain': domain,
                't00ls_username': username,
                't00ls_password': password
            })
    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"))
    print("共检测到", len(login_list), "个帐户, 开始获取积分")

    # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
    for i in range(len(login_list)):
        try:
            # 登录t00ls
            s,rlogin,rlogj = tslogin(push_config["t00ls_domain"], push_config["t00ls_username"], push_config["t00ls_password"], push_config["t00ls_qesnum"], push_config["t00ls_qan"])
            time.sleep(1)
            # 查询签到天数及活跃度
            tsactivity_main(s, push_config["t00ls_domain"])
            # 签到
            tsignin(s, push_config["t00ls_domain"], rlogj)
            time.sleep(1)
            # 域名查询
            domain_name_query(s, push_config["t00ls_domain"], rlogin, rlogj)
            
        except Exception as e:
            print("程序执行异常：" + str(e))
            
        continue

    print("程序执行完毕，获取积分过程结束")


if __name__ == '__main__':
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "【t00ls 签到】")
    t00ls_main()
