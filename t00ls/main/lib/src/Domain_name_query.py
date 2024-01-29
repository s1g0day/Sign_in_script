import json
import time
import urllib
import random
from datetime import datetime
from lib.src.getdomain import getdomain


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
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "今天已经查询过域名了!\n提示信息：",allreason)
            return True
        else:
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "今天还未查询过域名")
            return False

def Domain_name_query(s, domain, rlogin, rlogj):
    if not check_domain(s, domain, rlogin):
        frequency = 1
        while(frequency > 2):
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "域名查询失败")
        else:
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "尚未解决 cloudflare turnstile验证码")
            resjson = getdomain()
            for i in range(3):
                domainurl = resjson["data"]["list"][i]["domain"]
                print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "第[ %d ]次查询: `%s`" % (frequency,domainurl))
                frequency += 1

                
                # # 验证码识别
                
                # if(len(srcid) > 4): 
                #     print("验证码平台出错,错误信息: ", srcid)
                #     break
                # elif(len(srcid) < 4): 
                #     print("验证码识别错误： ", srcid)
                #     continue
                # else:
                #     print ('正在查询域名:', domainurl, "验证码为:", srcid)
                #     querydomainsubmit = urllib.parse.quote("查询")
                #     postdata = {
                #         'domain': domainurl,
                #         'formhash': rlogj["formhash"],
                #         'querydomainsubmit': querydomainsubmit,
                #         'seccodeverify': srcid
                #     }
                #     rpost = s.post(domain+'/domain.html', data=postdata)
                #     if ("域名查询可以积累域名的信息，为进一步了解做准备，不要为了TuBi而查询。" in rpost.text):
                #         print ("每日域名查询成功，+1 tubi！")
                #         break
                #     elif("Error:查询出错！域名不存在或接口有误，返回为空！" in rpost.text):
                #         print ("此域名:", domainurl, "不存在！")
                #         print('随机延时 5-10 秒，继续查询...')
                #         time.sleep(random.randint(5, 10))
                #         continue
                #     elif("Error:域名不符合规范3" in rpost.text):
                #         print ("域名不符合规范！")
                #         print('随机延时 5-10 秒，继续查询...')
                #         time.sleep(random.randint(5, 10))
                #         continue
                #     elif("持有人信息" in rpost.text):
                #         print ("域名查询成功,但未获得tubi,可能是域名不合格")
                #         print('随机延时 5-10 秒，继续查询...')
                #         time.sleep(random.randint(5, 10))
                #         continue
                #     else:
                #         print("未知报错")
                #         break
