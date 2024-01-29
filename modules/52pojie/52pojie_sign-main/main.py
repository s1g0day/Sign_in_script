#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: main.py(吾爱破解签到)
Author: Mrzqd
Date: 2023/2/4 08:00
cron: 30 7 * * *
new Env('吾爱破解签到');
"""
import os
import sys
from lib.notify import send
import urllib.parse
import requests
from bs4 import BeautifulSoup

def main():
    
    # 多cookie使用&分割
    cookies = "__bid_n=185576ed87aef8929f4207; wzws_sessionid=oGRLIaCBZDljNTQ0gDE4Mi4xMTkuMjMuMTU5gmRiMWNhYQ==; Hm_lvt_46d556462595ed05e05f009cdafff31a=1682216270,1682304737,1682326258,1682645412; FPTOKEN=3KtcjZbB+rTZzzyWQD3f3/GdtJSkKzS2JzRq1mWcRocMCTMQGQqpLFlo0L2we3c+VxjluAZTjuz7V2cbGxE870O3pRzBP1JKsld6BBKrxzwclLAuBHpjCivS6BAQxvNa4HS1sgz/crzGplyGLpyBNJMwE6EKTmM9hZjWU1cRFNaAQt28ptCQ1kzta9fOARCuKodo432OO4ZAQPcO5Dm7RdhjTkBV2J2Mx4GpkpK+/YjWFfZ6RO1Lqb983SIgyQPuOBe+9upZonEMteMwV3K7XCmesdvjhZu3r9CXYkzdxo5L1b2D7jgM/3xLeEaxt0qkULrDqsymU/OZGXLAvkj4XwLsjACGd2qt9izxtozR/2UGG/7dkqT48dPspgYK+SDWTMfo3p8XHKrauz1bZkWTpA==|empnRYfdYFG4wo9sEFQNR6tBqxdl6M7zDm+3rXS6hg8=|10|6dc657e3f84da7bb4a9678fb966bf0f8; __utma=15059762.1501646522.1682645585.1682645585.1682645585.1; __utmc=15059762; __utmz=15059762.1682645585.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); htVC_2132__refer=%252Fhome.php%253Fmod%253Dspacecp; htVC_2132_seccodecSAIpf=782387.0d411f20555e5ded09; htVC_2132_seccodecSAIpfRJE=782481.2c4bb349b2a0b6412e; htVC_2132_seccodecSAitm=787942.0d98c3a60483090c08; htVC_2132_seccodecSAitmao8=787943.5d7cc7c5b0810e71ee; htVC_2132_st_t=0%7C1682634043%7Cf527d7a1a49223daa03dc05952c44491; htVC_2132_forum_lastvisit=D_6_1682609074D_41_1682611004D_75_1682634043; BAIDU_SSP_lcr=http://zhannei.baidu.com/; htVC_2132_saltkey=f7oGE7Rz; htVC_2132_lastvisit=1682633082; htVC_2132_seccodecSAsQi=789033.30c168f623fa0c3340; htVC_2132_seccodecSAsQip3C=789032.f738767b46f0e9af1b; htVC_2132_ulastactivity=1682651447%7C0; htVC_2132_auth=2f17xVutxPFKA8Xp99%2FkVciP6%2B4yoHopFGznfrBJhZwgRv3NnA8hu5LqSSBJYJ%2Fg659pc5REKYrigCX7JcSq%2F9tXDHM; htVC_2132_lip=182.119.23.159%2C1682651447; htVC_2132_sid=0; htVC_2132_connect_is_bind=1; htVC_2132_ttask=624514%7C20230428; htVC_2132_noticonf=624514D1D3_3_1; htVC_2132_visitedfid=2D16; htVC_2132_st_p=624514%7C1682651911%7Ca67d25b88d78ddbe822378469baa2d39; htVC_2132_viewid=tid_1027420; wzws_cid=047b02781e16576d1d40705ce7292ba234c5eef1ac2bfeb6a2923313301fcf83bd222cd75782264c79bac63cb21e49174166669fafeac26febb611f3c89cd08611ea28d29b0017a67a56470cf199a5d5; htVC_2132_nofavfid=1; htVC_2132_lastact=1682652223%09home.php%09spacecp; htVC_2132_lastcheckfeed=624514%7C1682652223; htVC_2132_checkfollow=1; htVC_2132_checkpm=1; Hm_lpvt_46d556462595ed05e05f009cdafff31a=1682652239"
    n = 1
    for cookie in cookies.split("&"):
        url1 = "https://www.52pojie.cn/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWRyYXcmaWQ9Mg==?wzwscspd=MC4wLjAuMA=="
        url2 = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&referer=%2F'
        url3 = 'https://www.52pojie.cn/home.php?mod=task&do=draw&id=2'
        cookie = urllib.parse.unquote(cookie)
        cookie_list = cookie.split(";")
        cookie = ''
        for i in cookie_list:
            key = i.split("=")[0]
            if "htVC_2132_saltkey" in key:
                cookie += "htVC_2132_saltkey=" + urllib.parse.quote(i.split("=")[1]) + "; "
            if "htVC_2132_auth" in key:
                cookie += "htVC_2132_auth=" + urllib.parse.quote(i.split("=")[1]) + ";"
        if not ('htVC_2132_saltkey' in cookie or 'htVC_2132_auth' in cookie):
            print("第{n}cookie中未包含htVC_2132_saltkey或htVC_2132_auth字段，请检查cookie")
            sys.exit()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/109.0.0.0 Safari/537.36",
        }
        r = requests.get(url1, headers=headers, allow_redirects=False)
        s_cookie = r.headers['Set-Cookie']
        cookie = cookie + s_cookie
        headers['Cookie'] = cookie
        r = requests.get(url2, headers=headers, allow_redirects=False)
        s_cookie = r.headers['Set-Cookie']
        cookie = cookie + s_cookie
        headers['Cookie'] = cookie
        r = requests.get(url3, headers=headers)
        r_data = BeautifulSoup(r.text, "html.parser")
        jx_data = r_data.find("div", id="messagetext").find("p").text
        if "您需要先登录才能继续本操作" in jx_data:
            message = f"第{n}个账号Cookie 失效"
            # return f"第{n}个账号Cookie 失效"
        elif "恭喜" in jx_data:
            message = f"第{n}个账号签到成功"
            # return f"第{n}个账号签到成功"
        elif "不是进行中的任务" in jx_data:
            message = f"第{n}个账号今日已签到"
            # return f"第{n}个账号今日已签到"

        else:
            message = f"第{n}个账号签到失败"
            # return f"第{n}个账号签到失败"
        n += 1
        # print(message)
        send("吾爱签到", message)

if __name__ == '__main__':
    main()
