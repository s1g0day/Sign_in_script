# -*- coding: utf8 -*-
import re
import time
import math
import yaml
import random
from datetime import datetime
from requests import Session as req_Session
from modules.discuz.src.gen_anti_cc_cookies import gen_anti_cc_cookies_main

# 登录帐户
def login(domain: str, username: str, password: str):
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

# 查看是否已完成今日积分任务
def check_login_today_status(s: req_Session,  domain: str) -> bool:
    test_url = domain + "/home.php?mod=spacecp&ac=credit&op=log&suboperation=creditrulelog"
    res = s.get(test_url)
    res.raise_for_status()
    # 使用 re.findall 提取日期
    extracted_dates  = re.findall(r'<td>(\d{4}-\d{2}-\d{2}) \d{2}:\d{2}</td>', res.text)[0]
    if extracted_dates:
        current_date = datetime.now().date()
        
        # 将提取的日期字符串转换为 datetime 对象
        extracted_date = datetime.strptime(extracted_dates, '%Y-%m-%d').date()
        
        # 判断是否是当天日期
        if current_date == extracted_date:
            # print(f"{extracted_dates} 是当天日期")
            return True
        else:
            # print(f"{extracted_dates} 不是当天日期")
            return False
    else:
        print("未找到日期")

# 通过抓取用户设置页面的标题检查是否登录成功
def check_login_status(s: req_Session, number_c: int, domain: str, username:str) -> bool:
    test_url = domain + "/forum.php"
    res = s.get(test_url)
    res.raise_for_status()
    res_test = re.findall(r"charset = '(.*?)', discuz_uid = '(.*?)',", res.text)
    res.encoding = res_test[0][0]   # 编码 charset
    test_title = res_test[0][1]     # 用户id discuz_uid ,游客为 0
    if len(test_title) != 0:  # 确保正则匹配到了内容，防止出现数组索引越界的情况
        if(test_title != 0 ):
            print("第", number_c, "个帐户`", username, "`登录`", domain ,"`成功！")
            return True
        else:
            print("第", number_c, "个帐户`", username, "`登录`", domain ,"`失败！")
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

# 抓取并打印输出晋级用户组和所需积分
def Promotion_to_user_group(s: req_Session, domain: str):
    test_url = domain + "/home.php?mod=spacecp&ac=usergroup"
    res = s.get(test_url)
    res.raise_for_status()
    match_membership = re.search(r'<li id="c2">(.*?)</li>', res.text)
    match_score = re.search(r'您升级到此用户组还需积分 (\d+)', res.text)
    if match_membership and match_score:
        user_group = match_membership.group(1)
        # 使用字符串操作分割字符串
        groups = user_group.split(" - ")
        # 提取用户组
        membership = groups[1]
        score = match_score.group(1)
        score_day = math.ceil(int(score) / 20)
        result = "最多 `{}` 天就晋级 `{}` 了, 还需积分：`{}`".format(score_day, membership, score)
        print(result)
    else:
        print("无法获取用户组所需积分，可能页面存在错误或者未登录！")

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

        if check_login_today_status(s, domain):
            print("`", username, "`已完成今日积分任务")
        else:
            # 依次访问用户空间链接获取积分，出现错误时不中断程序继续尝试访问下一个链接
            for i in range(len(url_list)):
                url = url_list[i]
                try:
                    res = s.get(url)
                    res.raise_for_status()
                    res_test = re.findall(r"charset = '(.*?)', discuz_uid = '(.*?)',", res.text)
                    res.encoding = res_test[0][0]   # 编码 charset
                    test_title = re.findall(r"<title>(.*?)的个人资料", res.text)
            
                    print("第", i + 1, "个用户`", test_title[0], "`的空间链接访问成功")
                    time.sleep(5)  # 每访问一个链接后休眠5秒，以避免触发论坛的防CC机制
                except Exception as e:
                    print("链接访问异常：" + str(e))
                continue
            print_current_points(s, domain)  # 再次打印帐户当前积分
        Promotion_to_user_group(s, domain) # 获取晋级所需积分
    else:
        print("请检查你的帐户是否正确！")

def discuz_hostloc_main():

    # 加载配置
    push_config = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8").read())

    login_list = []
    for key in push_config:
        if key.startswith('discuz_hostloc_username'):
            index = key.split('discuz_hostloc_username')[1]
            domain = push_config['discuz_hostloc_domain']
            username = push_config['discuz_hostloc_username' + index]
            password = push_config['discuz_hostloc_password' + index]
            login_list.append({
                'discuz_hostloc_domain': domain,
                'discuz_hostloc_username': username,
                'discuz_hostloc_password': password
            })
    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"))
    print("共检测到", len(login_list), "个帐户, 开始获取积分")

    # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
    for i in range(len(login_list)):
        try:
            s = login(login_list[i]["discuz_hostloc_domain"], login_list[i]["discuz_hostloc_username"], login_list[i]["discuz_hostloc_password"])
            get_points(s, login_list[i]["discuz_hostloc_domain"], login_list[i]["discuz_hostloc_username"], i + 1 )
            
        except Exception as e:
            print("程序执行异常：" + str(e))
            
        continue

    print("程序执行完毕，获取积分过程结束")
