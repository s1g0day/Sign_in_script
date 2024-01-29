#!/usr/bin/python3
# -*- coding: utf8 -*-

import requests
import os
import subprocess
from urllib import parse
import warnings
warnings.filterwarnings("ignore")

def sendMessage(content):
    if(content != ""):
        server_data = {
            "title": "签到提醒",
            "desp": content
        }
        # telegram_bot = "https://api.telegram.org/botxxxxxx:xxxxxx/sendMessage"
        # res = requests.post(url=telegram_bot, data=tg_data)
        
        server_sauce = "https://sctapi.ftqq.com/xxxxxx"
        server_res = requests.post(url=server_sauce, data=server_data)
        print(server_res.text)

def filetg():
    filelist = traverse_dir("/root/signin/log")
    content = ""
    for filename in filelist:
        with open(filename, 'r', encoding="utf8") as file:
            # %0D%0A%0D%0A 作用于server酱的换行
            url_code_name = "%0D%0A%0D%0A"
            name = parse.unquote(url_code_name) 
            contentlist = file.readlines()
            for i in contentlist:
                content = content + i + name
    sendMessage(content)

def traverse_dir(path):
    pathlist = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            print("文件夹：", file_path)
            traverse_dir(file_path)
        elif "tixing" not in file_path:
            pathlist.append(file_path)
            #print("文件：", file_path)
    return pathlist
            
if __name__ == '__main__':
    filetg()
    print("0.tixing_server end")
