import json
from datetime import datetime

def tsignin(s, domain, rlogj):
    rurl = domain+'/ajax-sign.json'
    signdata = {'formhash': rlogj["formhash"], 'signsubmit': "true"}
    rsign = s.post(url=rurl, data=signdata)
    rsinj = json.loads(rsign.text)
    if (rsinj["status"] == "success"):
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "每日签到成功，+1 tubi！")
    elif (rsinj["message"] == "alreadysign"):
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "今天已经签到过了！")
    else:
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "签到失败（原因不明）！")
