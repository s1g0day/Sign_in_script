# -*- coding: utf8 -*-
import requests
import urllib.request
import json
import base64
import os
import string
from datetime import datetime
import time
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getdomain():
    '''
    爬取过期域名
    '''
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://ym.longming.com',
        'Pragma': 'no-cache',
        'Referer': 'https://ym.longming.com/delete/list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-forwarded-for': '183.225.180.6',
        'x-originating-ip': '183.225.180.6',
        'x-remote-addr': '183.225.180.6',
        'x-remote-ip': '183.225.180.6',
    }

    json_data = {
        'terraceFlag': 3,
        'pageNum': 1,
        'pageSize': 50,
        'include': {
            'name': '',
            'includeStart': False,
            'includeEnd': False,
        },
        'exclude': {
            'name': '',
            'excludeStart': False,
            'excludeEnd': False,
        },
        'deleteType': [],
        'suffixArray': [],
        'minSuffixLength': '',
        'maxSuffixLength': '',
        'deleteTime': time.strftime("%Y-%m-%d", time.localtime(time.time())),
        'regYear': '',
        'quick': '',
        'type': [],
        'isIDN': False,
        'myself': False,
        'special': '',
        'qqIntercept': '',
        'weixinIntercept': '',
        'minPR': '',
        'maxPR': '',
        'minOutLink': '',
        'maxOutLink': '',
        'domainType': 0,
        'sidx': 'delete_time',
        'order': 'asc',
    }

    response = requests.post('https://ym.longming.com/list/pre', headers=headers, json=json_data)
    resjson = json.loads(response.text)
    return resjson

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
    
    # 生成随机域名
    resjson = getdomain()
    for i in range(1):
        domainurl = resjson["data"]["list"][i]["domain"]
        print("未解决cloudflare 验证码,请手工查询域名: {%s}" %domainurl)


if __name__ == '__main__':
    print("*" * 30)
    start = int(time.time())
    main()
    stop = int(time.time())
    print("运行时间: ",stop-start,"s")
    print("*" * 30)
