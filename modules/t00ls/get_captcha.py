import os
import json
import base64
import random
import requests

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
