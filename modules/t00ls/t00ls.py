#!/usr/bin/python3
# -*- coding: utf8 -*-
# author: s1g0day
# create: 2025-02-27 00:00
# update: 2025-09-04 09:16
import re
import yaml
import time
import json
import urllib3
import requests
from datetime import datetime
from lib.logger_init import logger

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

# 检查今天是否已经查询过域名
def check_domain(s, domain, rlogin):
    today = datetime.now()
    if (rlogin != ""):
        tbreq = s.get(domain+'/members-tubilog.json')
        tblog = json.loads(tbreq.text)
        loglen = len(tblog["loglist"])
        allreason = ""
        for i in range(loglen):
            logday = tblog["loglist"][i]["timeline"]
            logdatetime = datetime.strptime(logday, "%Y-%m-%d %H:%M:%S")
            logdatetime = logdatetime.strftime("%Y-%m-%d")
            todaydate = today.strftime("%Y-%m-%d")
            if (logdatetime == todaydate):
                allreason += tblog["loglist"][i]["reason"]
            else:
                break
        if ("查询新com域名" in allreason):
            print("今天已经查询过域名了!\n提示信息：",allreason)
            logger.info(f"今天已经查询过域名了! 提示信息：{allreason}")
            return True
        else:
            print("今天还未查询过域名")
            logger.info("今天还未查询过域名")
            return False

# 域名查询
def domain_name_query(s, domain, rlogin, rlogj):
    if not check_domain(s, domain, rlogin):
        frequency = 1
        while(frequency > 2):
            print("域名查询失败")
            logger.warning("域名查询失败")
        else:
            print("尚未解决 cloudflare turnstile 验证码")
            logger.warning("尚未解决 cloudflare turnstile 验证码")
            # resjson = getdomain()
            # for i in range(3):
            #     domainurl = resjson["data"]["list"][i]["domain"]
            #     print("第[ %d ]次查询: `%s`" % (frequency,domainurl))
            #     frequency += 1

                # '''获取验证码'''
                # srcid = run(s, domain, tt_username, tt_password, tt_typeid)
                # print('正在查询域名:', domainurl, "验证码为:", srcid)
                # querydomainsubmit = urllib.parse.quote("查询")
                # postdata = {
                #     'domain': domainurl,
                #     'formhash': rlogj["formhash"],
                #     'querydomainsubmit': querydomainsubmit,
                #     'cf-turnstile-response': srcid
                # }
                # rpost = s.post(domain+'/domain.html', data=postdata)
                # if ("域名查询可以积累域名的信息，为进一步了解做准备，不要为了TuBi而查询。" in rpost.text):
                #     print("每日域名查询成功，+1 tubi！")
                #     break
                # elif("Error:查询出错！域名不存在或接口有误，返回为空！" in rpost.text):
                #     print("此域名:", domainurl, "不存在！")
                #     print('随机延时 5-10 秒，继续查询...')
                #     time.sleep(random.randint(5, 10))
                #     continue
                # elif("Error:域名不符合规范3" in rpost.text):
                #     print("域名不符合规范！")
                #     print('随机延时 5-10 秒，继续查询...')
                #     time.sleep(random.randint(5, 10))
                #     continue
                # elif("持有人信息" in rpost.text):
                #     print("域名查询成功,但未获得tubi,可能是域名不合格")
                #     print('随机延时 5-10 秒，继续查询...')
                #     time.sleep(random.randint(5, 10))
                #     continue
                # else:
                #     print("未知报错")
                #     break

def get_online_time(s, domain):
    """
    获取t00ls在线时间信息
    """
    try:
        checkurl = s.get(f'{domain}/checklogin.html')
        checkurl.raise_for_status()
        signbtn_datas = re.findall(r'a href="members-profile-(.+?).html" target', checkurl.text)
        if not signbtn_datas:
            print("未找到用户主页链接，可能未登录或页面结构已变")
            logger.error("未找到用户主页链接，可能未登录或页面结构已变")
            return
        spaceurl = s.get(f'{domain}/space-uid-{signbtn_datas[0]}.html')
        spaceurl.raise_for_status()
        # 提取在线时间
        match = re.search(r'<p>在线时间: 总计在线 <em>([\d.]+)</em> 小时, 本月在线 <em>([\d.]+)</em> 小时', spaceurl.text)
        # print(response1.text)
        if match:
            total_hours = match.group(1)
            month_hours = match.group(2)
            print(f"总计在线: {total_hours} 小时, 本月在线: {month_hours} 小时")
            logger.info(f"总计在线: {total_hours} 小时, 本月在线: {month_hours} 小时")
        else:
            print("未能提取在线时间信息，页面结构可能已变")
            logger.warning("未能提取在线时间信息，页面结构可能已变")
        
        # 提取积分信息
        points_match = re.search(r'<h3 class=\"blocktitle lightlink\">积分: ([\\d]+)</h3>', spaceurl.text)
        if points_match:
            print(f"积分: {points_match.group(1)}")
            logger.info(f"积分: {points_match.group(1)}")
        else:
            print("未能提取积分信息")
            logger.warning("未能提取积分信息")
        # 提取TCV, TuBi, 存款, 生杀币
        details_match = re.search(r'<p>TCV: ([\\d]+) ,&nbsp;TuBi: ([\\d]+) ,&nbsp;存款: ([\\d]+) ,&nbsp;生杀币: ([\\d]+) </p>', spaceurl.text)
        if details_match:
            print(f"TCV: {details_match.group(1)}, TuBi: {details_match.group(2)}, 存款: {details_match.group(3)}, 生杀币: {details_match.group(4)}")
            logger.info(f"TCV: {details_match.group(1)}, TuBi: {details_match.group(2)}, 存款: {details_match.group(3)}, 生杀币: {details_match.group(4)}")
        else:
            print("未能提取TCV, TuBi, 存款, 生杀币信息")
            logger.warning("未能提取TCV, TuBi, 存款, 生杀币信息")
    except Exception as e:
        print("get_online_time 异常:", e)
        logger.error(f"get_online_time 异常: {e}")

# 检查签到天数及活跃度
def tsactivity_main(s, domain):

    try:
        rurl = domain + '/members-profile.html'
        rsign = s.get(url=rurl)
        rsign.raise_for_status()  # 检查请求是否成功
        signbtn_datas = re.findall(r'disabled value="(.+?)"></h2>', rsign.text)
        activity_datas = re.findall(r'alt="(.+?)"', rsign.text)
        
        # 模糊匹配
        signbtn_search_string = '已签到'
        signbtn_matching_elements = [element for element in signbtn_datas if signbtn_search_string in element]

        if signbtn_matching_elements:
            print("签到天数: " + signbtn_datas[0])
            logger.info(f"签到天数: {signbtn_datas[0]}")
        else:
            print("未找到签到天数数据")
            logger.warning("未找到签到天数数据")

        # 模糊匹配
        activity_search_string = '活跃度'
        activity_matching_elements = [element for element in activity_datas if activity_search_string in element]

        if activity_matching_elements:
            print("活跃等级: " + activity_datas[1])
            logger.info(f"活跃等级: {activity_datas[1]}")
        else:
            print("未找到活跃等级数据")
            logger.warning("未找到活跃等级数据")
    except Exception as e:
        print("tsactivity_main 异常:", e)
        logger.error(f"tsactivity_main 异常: {e}")

# 签到
def tsignin(s, domain, rlogj):
    rurl = domain+'/ajax-sign.json'
    signdata = {'formhash': rlogj["formhash"], 'signsubmit': "true"}
    rsign = s.post(url=rurl, data=signdata)
    rsinj = json.loads(rsign.text)
    if (rsinj["status"] == "success"):
        print("每日签到成功，+1 tubi！")
        logger.info("每日签到成功，+1 tubi！")
    elif (rsinj["message"] == "alreadysign"):
        print("今天已经签到过了！")
        logger.info("今天已经签到过了！")
    else:
        print("签到失败（原因不明）！")
        logger.error("签到失败（原因不明）！")

# 登录
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
    rlogin = s.post(url=rurl, data=logindata, )
    rlogin.raise_for_status()
    rlogj = json.loads(rlogin.text)
    if (rlogj["status"] != "success"):
        print("登陆失败，信息错误")
        logger.error("登陆失败，信息错误")
    else:
        print(f"\n {uname} 登陆成功!")
        logger.info(f"{uname} 登陆成功!")
    return s,rlogin,rlogj

# 主程序
def t00ls_main():
    # 加载配置
    push_config = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8").read())

    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info(today.strftime("%Y-%m-%d %H:%M:%S"))
    print("共检测到", len(push_config['t00ls']), "个帐户, 开始获取积分")
    logger.info(f"共检测到{len(push_config['t00ls'])}个帐户, 开始获取积分")
    # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
    for i in range(len(push_config['t00ls'])):
        try:
            # 登录t00ls
            s,rlogin,rlogj = tslogin(push_config["t00ls_domain"], push_config['t00ls'][i]['username'], push_config['t00ls'][i]['password'], push_config['t00ls'][i]['qesnum'], push_config['t00ls'][i]['qan'])
            time.sleep(1)
            # 查询签到天数及活跃度
            tsactivity_main(s, push_config["t00ls_domain"])
            # 获取在线时间
            get_online_time(s, push_config["t00ls_domain"])
            time.sleep(1)
            # 签到
            tsignin(s, push_config["t00ls_domain"], rlogj)
            time.sleep(1)
            # 域名查询
            # domain_name_query(s, push_config["t00ls_domain"], rlogin, rlogj)
            
        except Exception as e:
            print("程序执行异常：" + str(e))
            logger.error(f"程序执行异常：{e}")
            
        continue

    print("程序执行完毕，获取积分过程结束")
    logger.info("程序执行完毕，获取积分过程结束")

# 主程序入口
if __name__ == '__main__':
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "【t00ls 签到】")
    logger.info(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "【t00ls 签到】")
    t00ls_main()