# -*- coding: utf8 -*-
import os
import time
import random
import re
import textwrap
import requests
import sys
import io
from datetime import datetime
from pyaes import AESModeOfOperationCBC
from requests import Session as req_Session


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


# 使用Python实现防CC验证页面中JS写的的toNumbers函数
def toNumbers(secret: str) -> list:
    text = []
    for value in textwrap.wrap(secret, 2):
        text.append(int(value, 16))
    return text


# 不带Cookies访问论坛首页，检查是否开启了防CC机制，将开启状态、AES计算所需的参数全部放在一个字典中返回
def check_anti_cc(domain: str) -> dict:
    result_dict = {}
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    res = requests.get(domain, headers=headers)
    aes_keys = re.findall(r'toNumbers\("(.*?)"\)', res.text)
    cookie_name = re.findall(r'cookie="(.*?)="', res.text)

    if len(aes_keys) != 0:  # 开启了防CC机制
        print("检测到防 CC 机制开启！")
        if len(aes_keys) != 3 or len(cookie_name) != 1:  # 正则表达式匹配到了参数，但是参数个数不对（不正常的情况）
            result_dict["ok"]    = 0
        else:  # 匹配正常时将参数存到result_dict中
            result_dict["ok"] = 1
            result_dict["cookie_name"] = cookie_name[0]
            result_dict["a"] = aes_keys[0]
            result_dict["b"] = aes_keys[1]
            result_dict["c"] = aes_keys[2]
    else:
        pass

    return result_dict


# 在开启了防CC机制时使用获取到的数据进行AES解密计算生成一条Cookie（未开启防CC机制时返回空Cookies）
def gen_anti_cc_cookies(domain: str) -> dict:
    cookies = {}
    anti_cc_status = check_anti_cc(domain)

    if anti_cc_status:  # 不为空，代表开启了防CC机制
        if anti_cc_status["ok"] == 0:
            print("防 CC 验证过程所需参数不符合要求，页面可能存在错误！")
        else:  # 使用获取到的三个值进行AES Cipher-Block Chaining解密计算以生成特定的Cookie值用于通过防CC验证
            print("自动模拟计尝试通过防 CC 验证")
            a = bytes(toNumbers(anti_cc_status["a"]))
            b = bytes(toNumbers(anti_cc_status["b"]))
            c = bytes(toNumbers(anti_cc_status["c"]))
            cbc_mode = AESModeOfOperationCBC(a, b)
            result = cbc_mode.decrypt(c)

            name = anti_cc_status["cookie_name"]
            cookies[name] = result.hex()
    else:
        pass

    return cookies


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
    s.cookies.update(gen_anti_cc_cookies(domain))
    res = s.post(url=login_url, data=login_data)
    res.raise_for_status()
    tsignin(s, domain)

    return s

def tsignin(s: req_Session, domain: str):

    test_url = domain + "/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"
    plugin = s.get(test_url).text
    if ("插件不存在" in plugin):
        print ("插件不存在或已关闭")
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
            print ("每日签到成功")
        elif ("已经签到" in rsinj):
            print ("今天已经签到过了！")
        else:
            print ("签到失败（原因不明）！")

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

def main():

    login_list = [
        {'domain': 'https://www.guokems.com', 'username': 'username', 'password': 'password'},
        # {'domain': 'https://hostloc.com', 'username': 'username', 'password': 'password'}
    ]
    
    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"))
    print("共检测到", len(login_list), "个网站, ", len(login_list), "个帐户, 开始获取积分")

    # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
    for i in range(len(login_list)):
        try:
            s = login(login_list[i]["domain"], login_list[i]["username"], login_list[i]["password"])
            get_points(s, login_list[i]["domain"], login_list[i]["username"] ,i + 1 )
            
        except Exception as e:
            print("程序执行异常：" + str(e))
            
        continue

    print("程序执行完毕，获取积分过程结束")

# def main_handler(event, context):
    # return main()


if __name__ == '__main__':
    print("*" * 30)
    start = int(time.time())
    main()
    stop = int(time.time())
    print("运行时间: ",stop-start,"s")
    print("*" * 30)