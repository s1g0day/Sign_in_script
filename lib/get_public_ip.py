import requests
from datetime import datetime

def getpublicip_ipify():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            data = response.json()
            ip = data['ip']
            return ip
        else:
            print('Failed to retrieve public IP')
    except requests.exceptions.RequestException as e:
        print('Error:', e)

def getpublicip_ping0():
    try:
        response = requests.get("http://ping0.cc/geo")
        if response.status_code == 200:
            # 将响应内容按行分割
            lines = response.text.splitlines()
            # 获取 IP 地址和位置信息
            ip_address = lines[0]
            location_info = lines[1]
            return ip_address, location_info
        else:
            print('Failed to retrieve public IP')
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        
def get_public_ip_main():
    # 调用函数获取公网IP
    public_ip, public_location = getpublicip_ping0()
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    if public_ip and public_location:
        print(f"IP: [{public_ip}](https://ping0.cc/ip/{public_ip})")
        print(f"location: {public_location}")
    else:
        print("Failed to retrieve public IP")

