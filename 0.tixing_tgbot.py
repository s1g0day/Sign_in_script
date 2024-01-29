#!/usr/bin/python3
# -*- coding: utf8 -*-

import os
import requests
import warnings
warnings.filterwarnings("ignore")

def sendMessage(content):
    if(content != ""):
        tg_data = {
            "chat_id": "chat_id",
            "parse_mode": "Markdown",
            "text": content,
            "disable_web_page_preview": "true",
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            }
        telegram_bot = "https://api.telegram.org/botxxxx:xxxx/sendMessage"
        res = requests.post(url=telegram_bot, data=tg_data, headers=headers)

def filetg():
    filelist = traverse_dir("signin/log")
    for filename in filelist:
        with open(filename, 'r', encoding="utf8") as file:
            content = ""
            contentlist = file.readlines()
            for i in contentlist:
                content = content + i
            sendMessage(content)
            print("\n","-"*15,"filename:",filename,"-"*15,"\ncontent:\n",contentlist)

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
    print("0.tixing_tgbot end")