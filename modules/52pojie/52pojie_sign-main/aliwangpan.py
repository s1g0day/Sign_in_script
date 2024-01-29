#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: aliwangpan.py(阿里网盘签到)
Author: Mrzqd
Date: 2023/2/19 14:25
cron: */10 * * 2 *
new Env('阿里网盘签到');
"""

import json
import logging
from lib.notify import send
import os
from datetime import datetime
from time import mktime, time
from typing import NoReturn

import requests


def update_access_token(refresh_token: str) -> bool | dict:
    """
    使用 refresh_token 更新 access_token

    :param refresh_token: refresh_token
    :return: 更新成功返回字典, 失败返回 False
    """
    data = requests.post(
        'https://auth.aliyundrive.com/v2/account/token',
        json={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
    ).json()

    try:
        if data['code'] in [
            'RefreshTokenExpired', 'InvalidParameter.RefreshToken',
        ]:
            logging.error(f'更新 access_token 失败, 错误信息: {data}')
            return False
    except KeyError:
        pass

    expire_time = datetime.strptime(data['expire_time'], '%Y-%m-%dT%H:%M:%SZ')

    return {
        'access_token': data['access_token'],
        'refresh_token': data['refresh_token'],
        'expired_at': int((mktime(expire_time.timetuple())) + 8 * 60 * 60) * 1000,
    }


def sign_in(access_token: str) -> bool:
    """
    签到函数

    :param access_token: access_token
    :return: 是否签到成功
    """
    data = requests.post(
        'https://member.aliyundrive.com/v1/activity/sign_in_list',
        headers={
            'Authorization': f'Bearer {access_token}',
        },
        json={},
    ).json()

    if 'success' not in data:
        logging.error(f'签到失败, 错误信息: {data}')
        return False

    current_day = None
    for i, day in enumerate(data['result']['signInLogs']):
        if day['status'] == 'miss':
            current_day = data['result']['signInLogs'][i - 1]
            break

    reward = (
        '无奖励'
        if not current_day['isReward']
        else f'获得 {current_day["reward"]["name"]} {current_day["reward"]["description"]}'
    )
    logging.info(f'签到成功, 本月累计签到 {data["result"]["signInCount"]} 天.')
    logging.info(f'本次签到 {reward}')
    mess = f'签到成功, 本月累计签到 {data["result"]["signInCount"]} 天. 本次签到 {reward}'
    # send("阿里云盘", mess)
    return True


def init_logger() -> NoReturn:
    """
    初始化日志系统

    :return:
    """
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log_format = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
    )

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(log_format)
    log.addHandler(ch)


def update_token_file(num: int, data: dict):
    """
    更新本地 access_token 文件

    :param data: data
    :param num: 第几个用户
    """
    num -= 1
    with open('aliconfig.json', 'r', encoding="utf-8") as f:
        config = json.load(f)
    config[num] = data
    with open('aliconfig.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(config, indent=4, ensure_ascii=False))


def main():
    # 判断是否存在文件
    if not os.path.exists('aliconfig.json'):
        base = [{"refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI0ODI4OGVjMzA1NjU0ODlkOTA4Y2U3NjQ3MDgzMGRiOCIsImN1c3RvbUpzb24iOiJ7XCJjbGllbnRJZFwiOlwiMjVkelgzdmJZcWt0Vnh5WFwiLFwiZG9tYWluSWRcIjpcImJqMjlcIixcInNjb3BlXCI6W1wiRFJJVkUuQUxMXCIsXCJTSEFSRS5BTExcIixcIkZJTEUuQUxMXCIsXCJVU0VSLkFMTFwiLFwiVklFVy5BTExcIixcIlNUT1JBR0UuQUxMXCIsXCJTVE9SQUdFRklMRS5MSVNUXCIsXCJCQVRDSFwiLFwiT0FVVEguQUxMXCIsXCJJTUFHRS5BTExcIixcIklOVklURS5BTExcIixcIkFDQ09VTlQuQUxMXCIsXCJTWU5DTUFQUElORy5MSVNUXCIsXCJTWU5DTUFQUElORy5ERUxFVEVcIl0sXCJyb2xlXCI6XCJ1c2VyXCIsXCJyZWZcIjpcImh0dHBzOi8vd3d3LmFsaXl1bmRyaXZlLmNvbS9cIixcImRldmljZV9pZFwiOlwiODUwMDg3ODFhOWIzNGZhNDg4ODY1MmFiOGVlZmM5NjlcIn0iLCJleHAiOjE2ODI2NTk2NzksImlhdCI6MTY4MjY1MjQxOX0.Ba8UPsMFs1FlLA5lmMrCQTiL7TTYzaQim60XS6gXD0n8kAiPUv6Bq491uhAWGRc-OrJf7aa1bfahFEBVZMOG_MJibaz-JED2gT1ZnuPL_CD9TUTGQKetFIHaFidemau89RmBXny9UxB3ap_A-Oo4VwcO9SADoImL_YLE5udwQlE", "is": 0}, {"refresh_token": "用户2refresh_token", "is": 0}]
        with open('aliconfig.json', 'w', encoding="utf-8") as f:
            f.write(json.dumps(base, indent=4, ensure_ascii=False))
    init_logger()  # 初始化日志系统
    with open('aliconfig.json', 'r', encoding="utf-8") as f:
        config = json.load(f)
    num = 0
    for user in config:
        num += 1
        if user['is'] == 0:
            logging.info(f'第{num}个 is值为0, 不进行任务')
            continue
        try:
            t = user['expired_at']
            access_token = user['access_token']
            sign_time = user['sign_time']
        except KeyError:
            t = 0
            access_token = None
            sign_time = None
        # 检查 access token 有效性
        if (
                int(t) < int(time() * 1000)
                or not access_token
        ):
            logging.info('access_token 已过期, 正在更新...')
            update_user = update_access_token(user['refresh_token'])
            if not update_user:
                logging.error('更新 access_token 失败.')
                user = {"refresh_token": "此refresh已失效", "is": 0}
                update_token_file(num, user)
                continue
            for i in update_user:
                user[i] = update_user[i]
            user['is'] = 1
            update_token_file(num, user)
        # 签到
        if sign_time == datetime.now().strftime('%Y-%m-%d'):
            logging.info('今日已签到, 跳过.')
            continue
        if not sign_in(user['access_token']):
            logging.error('签到失败.')
            mess = f'第{num}个用户签到失败'
            send("阿里云盘", mess)
            continue
        else:
            user["sign_time"] = datetime.now().strftime('%Y-%m-%d')
            update_token_file(num, user)


if __name__ == '__main__':
    main()
