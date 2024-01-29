import json
import urllib3
import requests

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
    rlogin = s.post(url=rurl, data=logindata, )
    rlogin.raise_for_status()
    rlogj = json.loads(rlogin.text)
    if (rlogj["status"] != "success"):
        print("登陆失败，信息错误")

    else:
        print(uname, "登陆成功!")
    return s,rlogin,rlogj
