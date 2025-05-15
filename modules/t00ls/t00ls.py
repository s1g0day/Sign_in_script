# -*- coding: utf-8 -*-

import re
import os
import yaml
import time
import json
import random
import string
import base64
import urllib3
import requests
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 
def get_captcha(s, domain):
    """
    获取验证码
    """
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
        'referer': domain+"/domain.html",
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }
    srcid = int(round(random.random()*10000))
    params = {
        'update': srcid,
    }

    # resp = requests.get(domain+'/seccode.php', params=params, cookies=cookies, headers=headers)
    resp = s.get(domain+'/seccode.php', params=params, headers=headers)
    if resp.status_code == 200:
        return resp.content
    else:
        print("接口返回值不是200")


def save_img(img_bytes):
    """
    保存图片到本地
    """
    tmp = str(random.randint(0,99999999)).zfill(8)
    filepath = ".\\img\\"+tmp+".png"
    with open(file=filepath, mode="wb") as f:
        f.write(img_bytes)
    return filepath

def base64_api(uname, pwd, img, typeid):
    """
    验证码的识别
    """
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    
    return ""

def run(s, domain, tt_username, tt_password, tt_typeid):
    '''
    # 一、图片文字类型(默认 3 数英混合)：
    # 1 : 纯数字
    # 1001：纯数字2
    # 2 : 纯英文
    # 1002：纯英文2
    # 3 : 数英混合
    # 1003：数英混合2
    #  4 : 闪动GIF
    # 7 : 无感学习(独家)
    # 11 : 计算题
    # 1005:  快速计算题
    # 16 : 汉字
    # 32 : 通用文字识别(证件、单据)
    # 66:  问答题
    # 49 :recaptcha图片识别
    # 二、图片旋转角度类型：
    # 29 :  旋转类型
    #
    # 三、图片坐标点选类型：
    # 19 :  1个坐标
    # 20 :  3个坐标
    # 21 :  3 ~ 5个坐标
    # 22 :  5 ~ 8个坐标
    # 27 :  1 ~ 4个坐标
    # 48 : 轨迹类型
    #
    # 四、缺口识别
    # 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
    # 33 : 单缺口识别（返回X轴坐标 只需要1张图）
    # 五、拼图识别
    # 53：拼图识别
    '''
    # username = "username"
    # password = "password"
    # typeid = 7

    print("----1: 获取验证码图片")
    img_bytes = get_captcha(s, domain)
    print("----2: 保存图片")
    img_path = save_img(img_bytes)
    print("----3: 识别图片")
    result = base64_api(uname=tt_username, pwd=tt_password, img=img_path, typeid=tt_typeid)
    print("----4: 识别完成删除图片")
    os.remove(img_path)

    if(len(result) > 4): 
        print("验证码平台出错,错误信息: ", result)
        return
    elif(len(result) < 4): 
        print("验证码识别错误： ", result)
        return
    else:
        return result

def random_domain():
    """
    生成随机域名
    """
    # 时间戳
    time_stamp = int(time.time())
    # 字符数字随机7位
    other = random.sample(string.ascii_lowercase+string.digits,7) #随机取7位
    # 格式化
    res = ''.join(other)+str(time_stamp)
    res1 = ''.join(random.sample(res,len(res)))
    # 拼接
    suffix = "xin|com|cn|net|com.cn|vip|top|cc|shop|club|wang|xyz|luxe|site|news|pub|fun|online|win|red|loan|ren|mom|net.cn|org|link|biz|bid|help|tech|date|mobi|so|me|tv|co|vc|pw|video|party|pics|website|store|ltd|ink|trade|live|wiki|space|gift|lol|work|band|info|click|photo|market|tel|social|press|game|kim|org.cn|games|pro|men|love|studio|rocks|asia|group|science|design|software|engineer|lawyer|fit|beer|我爱你|中国|公司|网络|在线|网址|网店|集团|中文网"
    liff = suffix.split("|")
    liffint = (random.randint(0,(len(liff))))
    # random_string = res1 + liffint
    random_string = "8970.cn"
    return random_string

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
            return True
        else:
            print("今天还未查询过域名")
            return False

def domain_name_query(s, domain, rlogin, rlogj):
    if not check_domain(s, domain, rlogin):
        frequency = 1
        while(frequency > 2):
            print("域名查询失败")
        else:
            print("尚未解决 cloudflare turnstile 验证码")
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
        else:
            print("未找到签到天数数据")

        # 模糊匹配
        activity_search_string = '活跃度'
        activity_matching_elements = [element for element in activity_datas if activity_search_string in element]

        if activity_matching_elements:
            print("活跃等级: " + activity_datas[1] + "\n")
        else:
            print("未找到活跃等级数据")

    
    except requests.exceptions.RequestException as e:
        print("tsactivity_main 请求异常:", e)
    except (IndexError, KeyError) as e:
        print("tsactivity_main 数据提取异常:", e)

# 签到
def tsignin(s, domain, rlogj):
    rurl = domain+'/ajax-sign.json'
    signdata = {'formhash': rlogj["formhash"], 'signsubmit': "true"}
    rsign = s.post(url=rurl, data=signdata)
    rsinj = json.loads(rsign.text)
    if (rsinj["status"] == "success"):
        print("每日签到成功，+1 tubi！")
    elif (rsinj["message"] == "alreadysign"):
        print("今天已经签到过了！")
    else:
        print("签到失败（原因不明）！")

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

    else:
        print(uname, "登陆成功!")
    return s,rlogin,rlogj

def t00ls_main():
    # 加载配置
    push_config = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8").read())

    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"))
    print("共检测到", len(push_config['t00ls']), "个帐户, 开始获取积分")

    # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
    for i in range(len(push_config['t00ls'])):
        try:
            # 登录t00ls
            s,rlogin,rlogj = tslogin(push_config["t00ls_domain"], push_config['t00ls'][i]['username'], push_config['t00ls'][i]['password'], push_config['t00ls'][i]['qesnum'], push_config['t00ls'][i]['qan'])
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
