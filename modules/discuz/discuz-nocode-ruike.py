# -*- coding: utf8 -*-
import re
import yaml
import time
import random
from datetime import datetime
from requests import Session as req_Session
from modules.discuz.gen_anti_cc_cookies import gen_anti_cc_cookies_main

# 登录帐户
def login(domain: str, username: str, password: str) -> req_Session:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0",
        "origin": domain,
        "referer": domain + "/forum.php"
    }
    login_url = domain + "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    login_data = {
        "fastloginfield": "username",
        "username": username,
        "password": password,
        "quickforward": "yes",
        "handlekey": "ls"

    }

    s = req_Session()
    s.headers.update(headers)
    s.cookies.update(gen_anti_cc_cookies_main(domain))
    res = s.post(url=login_url, data=login_data)
    res.raise_for_status()
    tsignin(s, domain)

    return s

def tsignin(s: req_Session, domain: str):

    test_url = domain + "/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"
    plugin = s.get(test_url).text
    if ("插件不存在" in plugin):
        print("签到插件不存在或已关闭")
        return False
    else:
        signdata = {
            "formhash": "cb829ca3",
            "qdxq": "kx",
            "qdmode": "2",
            "todaysay": "",
            "fastreply": "0"
        }
        cookie = {"cookie": 
            "DJRR_2132_saltkey=wLL6H7I8; DJRR_2132_auth=6fd2eG8dsJmDvuHCdXNP0n7Kh3ggIYiZxW3iohwWQ9u22zWb6iDjv7mNjAmf3%2BG26Rk4E7kAP37GWZ%2Fdhca7yrYi;"
        }
        rsign = s.post(url=test_url, data=signdata,headers=cookie)
        rsign.raise_for_status()
        rsinj = rsign.text
        print("*" * 30)
        if ("签到成功" in rsinj):
            print("每日签到成功")
        elif ("已经签到" in rsinj):
            print("今天已经签到过了！")
        else:
            print("签到失败（原因不明）！")

# 通过抓取用户设置页面的标题检查是否登录成功
def check_login_status(s: req_Session, number_c: int, domain: str, username:str) -> bool:
    test_url = domain + "/forum.php"
    res = s.get(test_url)
    res.raise_for_status()
    res_test = re.findall(r"charset = '(.*?)', discuz_uid = '(.*?)',", res.text)
    res.encoding = res_test[0][0]   # 编码 charset
    test_title = res_test[0][1]     # 用户id discuz_uid ,游客为 0
    if len(test_title) != 0:  # 确保正则匹配到了内容，防止出现数组索引越界的情况
        if(test_title[0] != 0):
            print("第", number_c, "个帐户[", username, "]登录[", domain ,"]成功！")
            return True
        else:
            print("第", number_c, "个帐户[", username, "]登录[", domain ,"]失败！")
            return False
    else:
        print("无法在用户设置页面找到标题，该页面存在错误或被防 CC 机制拦截！")
        return False


# 抓取并打印输出帐户当前积分
def print_current_points(s: req_Session, domain: str):
    test_url = domain + "/forum.php"
    res = s.get(test_url)
    res.raise_for_status()
    res_test = re.findall(r"charset = '(.*?)', discuz_uid = '(.*?)',", res.text)
    res.encoding = res_test[0][0]   # 编码 charset
    points = re.findall(r"积分: (\d+)", res.text)

    if len(points) != 0:  # 确保正则匹配到了内容，防止出现数组索引越界的情况
        print("帐户当前积分：" + points[0])
    else:
        print("无法获取帐户积分，可能页面存在错误或者未登录！")
    time.sleep(5)

# 随机生成用户空间链接
def randomly_gen_uspace_url(domain: str) -> list:
    url_list = []
    # 访问小黑屋用户空间不会获得积分、生成的随机数可能会重复，这里多生成两个链接用作冗余
    for i in range(12):
        uid = random.randint(1, 3000)
        url = domain + "/home.php?mod=space&uid={}&do=profile&from=space".format(str(uid))
        url_list.append(url)
        i += 1
    return url_list


# 依次访问随机生成的用户空间链接获取积分
def get_points(s: req_Session, domain: str, username: str, number_c: int):
    if check_login_status(s, number_c, domain ,username):
        print_current_points(s, domain)  # 打印帐户当前积分
        url_list = randomly_gen_uspace_url(domain)

        # 依次访问用户空间链接获取积分，出现错误时不中断程序继续尝试访问下一个链接
        for i in range(len(url_list)):
            url = url_list[i]
            try:
                res = s.get(url)
                res.raise_for_status()
                res_test = re.findall(r"charset = '(.*?)', discuz_uid = '(.*?)',", res.text)
                res.encoding = res_test[0][0]   # 编码 charset
                test_title = re.findall(r"<title>(.*?)的个人资料", res.text)
        
                print("第", i + 1, "个用户", test_title[0], "的空间链接访问成功")
                time.sleep(5)  # 每访问一个链接后休眠5秒，以避免触发论坛的防CC机制
            except Exception as e:
                print("链接访问异常：" + str(e))
            continue
        print_current_points(s, domain)  # 再次打印帐户当前积分
    else:
        print("请检查你的帐户是否正确！")

def discuz_ruike_main():
    # 加载配置
    push_config = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8").read())

    login_list = []
    for key in push_config:
        if key.startswith('discuz_ruike_username'):
            index = key.split('discuz_ruike_username')[1]
            domain = push_config['discuz_ruike_domain']
            username = push_config['discuz_ruike_username' + index]
            password = push_config['discuz_ruike_password' + index]
            login_list.append({
                'discuz_ruike_domain': domain,
                'discuz_ruike_username': username,
                'discuz_ruike_password': password
            })
    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"))
    print("共检测到", len(login_list), "个帐户, 开始获取积分")

    # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
    for i in range(len(login_list)):
        try:
            s = login(login_list[i]["discuz_ruike_domain"], login_list[i]["discuz_ruike_username"], login_list[i]["discuz_ruike_password"])
            get_points(s, login_list[i]["discuz_ruike_domain"], login_list[i]["discuz_ruike_username"], i + 1 )
            
        except Exception as e:
            print("程序执行异常：" + str(e))
            
        continue

    print("程序执行完毕，获取积分过程结束")
