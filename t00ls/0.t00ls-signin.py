# -*- coding: utf8 -*-

import json
import urllib3
import requests
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def tsignin(s, domain, rlogj):
    rurl = domain+'/ajax-sign.json'
    signdata = {'formhash': rlogj["formhash"], 'signsubmit': "true"}
    rsign = s.post(url=rurl, data=signdata)
    rsinj = json.loads(rsign.text)
    if (rsinj["status"] == "success"):
        print ("每日签到成功，+1 tubi！")
    elif (rsinj["message"] == "alreadysign"):
        print ("今天已经签到过了！")
    else:
        print ("签到失败（原因不明）！")

def tslogin(domain, uname, pswd, qesnum, qan):

    logindata = {
        'action': 'login',
        'username': uname,
        'password': pswd,
        'questionid': qesnum,
        'answer': qan
    }
    rurl=domain+"/login.json"
    s = requests.session()
    rlogin = s.post(url=rurl, data=logindata)
    rlogin.raise_for_status()
    rlogj = json.loads(rlogin.text)
    if (rlogj["status"] != "success"):
        print ("登陆失败，信息错误")
    else:
        print(uname, "登陆[",domain,"]成功!")
    return s,rlogj

def main():
    domain = "https://www.t00ls.com"
    uname = 'uname'  # 帐号
    pswd = 'pswd'  # 密码
    qesnum = 1  # 安全提问 参考下面
    qan = 'qan'  # 安全提问答案

    # 0 = 没有安全提问
    # 1 = 母亲的名字
    # 2 = 爷爷的名字
    # 3 = 父亲出生的城市
    # 4 = 您其中一位老师的名字
    # 5 = 您个人计算机的型号
    # 6 = 您最喜欢的餐馆名称
    # 7 = 驾驶执照的最后四位数字
    
    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"))
    # 登录
    s,rlogj = tslogin(domain, uname, pswd, qesnum, qan)
    # 签到
    tsignin(s, domain, rlogj)


if __name__ == '__main__':
    main()
