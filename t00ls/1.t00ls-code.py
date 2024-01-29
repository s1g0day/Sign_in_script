# -*- coding: utf8 -*-



import os
import time
import json
import base64
import random
import string
import urllib3
import requests
import urllib.request
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def run(s, domain):
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
    username = "username"
    password = "password"
    typeid = 7
    
    print("----1: 获取验证码图片")
    img_bytes = get_captcha(s, domain)
    print("----2: 保存图片")
    img_path = save_img(img_bytes)
    print("----3: 识别图片")
    result = base64_api(uname=username, pwd=password, img=img_path, typeid=typeid)
    print("----4: 识别完成删除图片")
    os.remove(img_path)
    return result


def randdm():
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


def Domain_name_query(s, domain, rlogin, today, rlogj):
    
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
        else:
            print("今天还未查询过域名")
            frequency = 1
            while(frequency > 2):
                print("域名查询失败")
            else:
                print("第[ %d ]次查询: " % frequency)
                frequency += 1
                # domainurl = randdm()
                resjson = getdomain()
                for i in range(3):
                    domainurl = resjson["data"]["list"][i]["domain"]
                    srcid = run(s, domain)
                    if(len(srcid) > 4): 
                        print("验证码平台出错,错误信息: ", srcid)
                        break
                    elif(len(srcid) < 4): 
                        print("验证码识别错误： ", srcid)
                        continue
                    else:
                        print ('正在查询域名:', domainurl, "验证码为:", srcid)
                        querydomainsubmit = urllib.parse.quote("查询")
                        postdata = {
                            'domain': domainurl,
                            'formhash': rlogj["formhash"],
                            'querydomainsubmit': querydomainsubmit,
                            'seccodeverify': srcid
                        }
                        rpost = s.post(domain+'/domain.html', data=postdata)
                        if ("域名查询可以积累域名的信息，为进一步了解做准备，不要为了TuBi而查询。" in rpost.text):
                            print ("每日域名查询成功，+1 tubi！")
                            break
                        elif("Error:查询出错！域名不存在或接口有误，返回为空！" in rpost.text):
                            print ("此域名:", domainurl, "不存在！")
                            print('随机延时 5-10 秒，继续查询...')
                            time.sleep(random.randint(5, 10))
                            
                        elif("Error:验证码不正确！" in rpost.text):
                            print ("验证码不正确！")
                            print('随机延时 5-10 秒，继续查询...')
                            time.sleep(random.randint(5, 10))
                            continue
                        elif("Error:域名不符合规范3" in rpost.text):
                            print ("域名不符合规范！")
                            print('随机延时 5-10 秒，继续查询...')
                            time.sleep(random.randint(5, 10))
                            
                        elif("持有人信息" in rpost.text):
                            print ("域名查询成功,但未获得tubi,可能是域名不合格")
                            print('随机延时 5-10 秒，继续查询...')
                            time.sleep(random.randint(5, 10))
                            continue
                        else:
                            print("未知报错")
                            break

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
    return s,rlogin,rlogj

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
    s,rlogin,rlogj = tslogin(domain, uname, pswd, qesnum, qan)
    # 签到
    
    tsignin(s, domain, rlogj)

    Domain_name_query(s, domain, rlogin, today, rlogj)

if __name__ == '__main__':
    print("*" * 30)
    start = int(time.time())
    main()
    stop = int(time.time())
    print("运行时间: ",stop-start,"s")
    print("*" * 30)
