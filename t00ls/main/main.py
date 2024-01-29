# -*- coding: utf-8 -*-

import time
from lib.common.config import config
from lib.src.tslogin import tslogin
from lib.src.tsignin import tsignin
from lib.src.getdomain import getdomain
from lib.src.Domain_name_query import Domain_name_query

def main():

    # 获取配置
    push_config = config()
    
    # 登录t00ls
    s,rlogin,rlogj = tslogin(push_config.get('domain'), push_config.get('uname'), push_config.get('pswd'), push_config.get('qesnum'), push_config.get('qan'))
    time.sleep(1)
    # 签到
    tsignin(s, push_config.get('domain'), rlogj)
    time.sleep(1)
    # 域名查询
    Domain_name_query(s, push_config.get('domain'), rlogin, rlogj)



if __name__ == '__main__':
    print("t00ls 签到")
    main()
