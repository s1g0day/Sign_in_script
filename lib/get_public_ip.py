import requests
from datetime import datetime

def get_public_ip():
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
        
def get_public_ip_main():
    # 调用函数获取公网IP
    public_ip = get_public_ip()
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    if public_ip:
        print(f"服务器的公网IP是: `{public_ip}`")
    else:
        print("无法获取服务器的公网IP")
