import requests

def try_ip():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://api.ip.sb/ip', headers=headers)
        public_ip = response.text.strip()
        return public_ip
    except requests.RequestException:
        return None

def get_ip_main():
    # 调用函数获取公网IP
    public_ip = try_ip()
    if public_ip:
        print("服务器: `%s`" %public_ip)
    else:
        print("无法获取服务器的公网IP")
# main()