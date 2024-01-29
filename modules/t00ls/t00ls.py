# -*- coding: utf-8 -*-

import time
from datetime import datetime
from lib.config import config
from modules.t00ls.src.tslogin import tslogin
from modules.t00ls.src.tsignin import tsignin
from modules.t00ls.src.tsactivity import tsactivity_main
from modules.t00ls.src.domain_query import domain_name_query

def t00ls_main():

    # 获取配置
    push_config = config()
    
    # 登录t00ls
    s,rlogin,rlogj = tslogin(push_config.get('t00ls_domain'), push_config.get('t00ls_uname'), push_config.get('t00ls_pswd'), push_config.get('t00ls_qesnum'), push_config.get('t00ls_qan'))
    time.sleep(1)
    # 查询签到天数及活跃度
    tsactivity_main(s,push_config.get('t00ls_domain'))
    # 签到
    tsignin(s, push_config.get('t00ls_domain'), rlogj)
    time.sleep(1)
    # 域名查询
    domain_name_query(s, push_config.get('t00ls_domain'), rlogin, rlogj)



if __name__ == '__main__':
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "【t00ls 签到】")
    t00ls_main()
