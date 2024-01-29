import time
import json
import random
import string
import requests


def random_domain():
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
