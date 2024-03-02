import json

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
