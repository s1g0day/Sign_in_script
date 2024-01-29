import json
import urllib3
import requests
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "登陆失败，信息错误")

    else:
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + uname, "登陆成功!")
    return s,rlogin,rlogj
