#Filename: threatbook_auto.py
#Author: s1g0day
#Date: 2024/12/19
#Update: 2025/05/14
#Description: 微步在线自动点赞、关注、签到获取经验值+1脚本


import re
import yaml
import json
import time
import random
import urllib3
import requests
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ThreatbookAuto:
    def __init__(self):
        self.push_config = yaml.safe_load(open(r"config/config.yaml", "r", encoding="utf-8").read())
        self.COOKIE = self.get_threatbook_cookie()
        self.x_csrf_token, self.xx_csrf = self.get_csrf_token(self.COOKIE)
        self.session = requests.Session()
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/json',
            'Cookie': self.COOKIE,
            'Origin': self.push_config['threatbook_domain'],
            'Referer': self.push_config['threatbook_domain'],
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.87'
                          'Safari/537.36 SE 2.X MetaSr 1.0',
            'X-CSRF-Token': self.x_csrf_token,
            'Xx-Csrf': self.xx_csrf
        }

    def send_request(self, method, url, data=None, params=None):
        """
        通用请求函数，支持GET和POST请求
        :param method: 请求方法 ('GET' 或 'POST')
        :param url: 请求URL
        :param data: POST请求的数据
        :param params: GET请求的参数
        :return: 请求响应对象，失败时返回None
        """
        try:
            if method.upper() == 'GET':
                # time.sleep(random.random() * 5)  # 仅GET请求添加随机延迟
                response = self.session.get(
                    url=url,
                    headers=self.session.headers,
                    params=params,
                    verify=False,
                    allow_redirects=False
                )
            elif method.upper() == 'POST':
                response = self.session.post(
                    url=url,
                    headers=self.session.headers,
                    data=data,
                    params=params,
                    verify=False,
                    allow_redirects=False
                )
            else:
                raise ValueError(f"不支持的请求方法: {method}")

            response.encoding = response.apparent_encoding
            response.raise_for_status()  # 检查HTTP状态码
            # 检查是不是json
            if "gradeIntroduction" not in url and not response.text.startswith('{'):
                print("服务器返回非JSON响应")
                return None
            return response
        except Exception as e:
            print(f"\r\t\033[1;31m{method}请求网络出错：{str(e)}\033[0m")
            return None

    # 获取threatbook_cookie
    def get_threatbook_cookie(self):
        threatbook_cookie = self.push_config['threatbook_cookie']
        if threatbook_cookie:
            return threatbook_cookie
        return threatbook_cookie
    # 获取csrf_token和xx_csrf
    def get_csrf_token(self, cookie: str):
        # 定义Cookie字符串
        # 使用正则表达式从Cookie中提取值
        csrf_token_match = re.search(r'csrfToken=([^;]+)', cookie)
        xx_csrf_match = re.search(r'xx-csrf=([^;]+)', cookie)

        # 获取并打印值
        x_csrf_token = csrf_token_match.group(1) if csrf_token_match else None
        xx_csrf = xx_csrf_match.group(1) if xx_csrf_match else None

        return x_csrf_token, xx_csrf

    # 获取用户数据
    def get_user_data(self, user_id: str):
        user_api = f"{self.push_config['threatbook_domain']}/v5/node/community/user/icon/{user_id}"
        response = self.send_request('GET', user_api)
        if response and response.text:
            return response.json()
        return None

    # 获取我的信息
    def get_my_info(self):
        my_info_api = f"{self.push_config['threatbook_domain']}/v5/node/intelServiceCenter/queryMyKey"
        response = self.send_request('GET', my_info_api)
        if response and response.text:
            res_json = response.json()
            if res_json['response_code'] == 0 and res_json['verbose_msg'] == 'succeed':
                return res_json.get('data')
        return None
    # 获取等级介绍
    def get_gradeIntroduction_info(self):
        try:
            gradeIntroduction_api = f"{self.push_config['threatbook_domain']}/v5/gradeIntroduction"
            response = self.send_request('GET', gradeIntroduction_api)
            if not response or not response.text:
                raise Exception("请求失败或返回为空")
            # 解析HTML内容
            html_content = response.text
            # 使用正则表达式提取JSON数据
            json_data_match = re.search(r'window\.__INITIAL_STATE__= (\{.*?\});', html_content)
            if json_data_match:
                json_data = json.loads(json_data_match.group(1))
                # 获取当前积分和下一个等级积分
                level = json_data['data']['userInfo']['level']
                exp = json_data['data']['userInfo']['exp']  # 当前积分
                totalExp = json_data['data']['userInfo']['totalExp']  # 下一个等级所需积分
                
                # 计算升级所需的差值
                exp_needed = totalExp - exp
                
                print(f"当前等级: {level} | 当前积分: {exp} | 下一个等级所需积分: {totalExp} | 升级所需差值: {exp_needed}")
            else:
                print("未找到JSON数据")
        except Exception as e:
            print(f"获取等级介绍失败：{e}")
            self.get_level_info()
        
        
    # 获取等级信息
    def get_level_info(self):
        level_api = f"{self.push_config['threatbook_domain']}/v5/node/enterprise/getTopList"
        response = self.send_request('GET', level_api)
        if response and response.text:
            res_json = response.json()
            if res_json['response_code'] == 0 and res_json['verbose_msg'] == 'succeed':
                return res_json['data']['total']
            print(f'等级信息获取失败：{res_json}')
        return None

    # 获取成长值信息
    def get_point_info(self):
        point_api = f"{self.push_config['threatbook_domain']}/v5/node/enterprise/getTableList"
        page = 0
        today_point_list = []
        # 获取当前日期
        today_date = datetime.now().strftime("%Y-%m-%d")
        print('正在获取今日成长值信息...')
        while True:
            params = {
                'page': page
            }
            response = self.send_request('GET', point_api, params=params)
            if not response or not response.text:
                break
            
            res_json = response.json()
            data = res_json.get('point_list')
            if res_json.get('response_code') != 0 or not data:
                break

            # 遍历当前页的数据
            for item in data:
                if item['ctime'].startswith(today_date):
                    today_point_list.append(item)
                else:
                    break

            # 如果当前页所有元素都是当天的，继续下一页
            page += 1

        today_point_list.reverse()
        today_total_point = 0
        # 创建一个字典来存储统计结果
        stats = {}
        for item in today_point_list:
            action = item["actionDesc"]
            point = item["point"]
            if action not in stats:
                stats[action] = {
                    "count": 0,
                    "total_points": 0
                }
            stats[action]["count"] += 1
            stats[action]["total_points"] += point
            today_total_point += item['point']

        # 动态生成日志内容
        details = []
        for action, summary in stats.items():
            details.append(f"{action}×{summary['count']}：{'+' if summary['total_points'] > 0 else ''}{summary['total_points']}")

        details_str = " | ".join(details)
        print(f"今日获取总成长值：{today_total_point} | {details_str}")
        return today_total_point, details_str

    # 获取主页数据
    def get_article_data(self):
        article_api = f"{self.push_config['threatbook_domain']}/v5/node/community/infoFlow/page"
        page = 1
        last_threat_id = ''
        article_list = []
        like_list = []
        follow_list = []
        print('开始获取主页数据...')
        # 获取主页数据
        while True:
            # 必选参数
            params = {
                'classify': 'all',
                'page': page,
                'pageSize': 10
            }
            if last_threat_id:
                params['lastThreatId'] = last_threat_id
            response = self.send_request('GET', article_api, params=params)
            if not response or not response.text:
                break
                
            res_json = response.json()
            if response.json()['response_code'] == 0 or response.json()['verbose_msg'] == 'succeed':
                res_data = res_json.get('data')
                if not res_data:
                    break

                # 更新 last_threat_id 和 article_list
                last_threat_id = res_data[-1]['articleInfo']['bid']
                article_list.extend(res_data)

                # 更新待点赞文章列表和待关注用户列表
                for article in res_data:
                    if not article['articleInfo']['praised'] and len(like_list) < 15:
                        like_list.append(article['articleInfo']['threatId'])

                    user_id = article['userInfo']['userId']
                    user_data = self.get_user_data(user_id)
                    if user_data and not user_data['data']['isFollowed'] and len(follow_list) < 5:
                        follow_list.append({
                            'user_id': user_id,
                            'user_name': user_data['data']['userName']
                        })

                    # 如果两个列表都达到目标长度，退出循环
                    if len(like_list) >= 10 and len(follow_list) >= 3:
                        break

                # 检查article_list中待点赞文章数和待关注用户数够不够
                if len(like_list) >= 10 and len(follow_list) >= 3:
                    break

                page += 1
                sleep_time = random.uniform(0.1, 1)
                time.sleep(sleep_time)

        return article_list, like_list, follow_list

    def like(self, like_list):
        """
        每日点赞文章 +5成长值/篇
        限制：每日最多加10篇点赞分
        """
        print('开始点赞...')
        total = self.get_level_info()
        if total is None:
            print("获取等级信息失败，中止点赞")
            return
            
        for index, article_id in enumerate(like_list):
            like_api = f"{self.push_config['threatbook_domain']}/v5/node/user/like"
            like_data = {
                'id': f'{article_id}',
                'option': '0'
            }
            response = self.send_request('POST', like_api, data=json.dumps(like_data))
            if response and response.text:
                res_json = response.json()
                if res_json['response_code'] == 0 and res_json['verbose_msg'] == 'OK':
                    total_now = self.get_level_info()
                    if total_now == total:
                        print("今日成长值已达上限，中止点赞")
                        break
                    if index < 10:
                        print(f"点赞成功{index + 1}/{len(like_list)}：文章id {article_id} +5成长值")
                    else:
                        print(f"点赞成功{index + 1}/{len(like_list)}：文章id {article_id} 今日点赞成长值已达上限")
                else:
                    print(f"点赞失败{index + 1}/{len(like_list)}：文章id {article_id}, {res_json}")
            else:
                print(f"点赞失败{index + 1}/{len(like_list)}：文章id {article_id}, 请求失败")
            sleep_time = random.uniform(0.5, 2)
            time.sleep(sleep_time)

    def follow(self, follow_list):
        """
        每日关注用户 +5成长值/人
        限制：每日最多加3人分
        """
        print('开始关注...')
        for index, user in enumerate(follow_list):
            user_id = user['user_id']
            user_name = user['user_name']
            follow_api = f"{self.push_config['threatbook_domain']}/v5/node/community/userFollow/change/{user_id}"
            params = {
                'operation': 'follow'
            }
            if index < 3:
                response = self.send_request('POST', follow_api, params=params)
                if response and response.text:
                    res_json = response.json()
                    if res_json['response_code'] == 0 and res_json['verbose_msg'] == 'OK':
                        print(f"关注成功{index + 1}/{len(follow_list)}：{user_name} +5成长值")
                    else:
                        print(f"关注失败{index + 1}/{len(follow_list)}：{user_name}, {res_json}")
                else:
                    print(f"关注失败{index + 1}/{len(follow_list)}：{user_name}, 请求失败")
            else:
                print(f"关注成功{index + 1}/{len(follow_list)}：{user_name} 今日关注成长值已达上限")
            sleep_time = random.uniform(0.5, 2)
            time.sleep(sleep_time)

    # 为fish_reminder.py提供数据
    def fish_reminder_send_article(self, content):
        try:
            send_data = {
                'anonymous': False,
                'content': content,
                'iocList': [],
                'imgList': [],
                'sampleList': [],
                'fileList': [],
            }
            article_save_api = f"{self.push_config['threatbook_domain']}/v5/node/user/article/save"
            response = self.send_request('POST', article_save_api, data=json.dumps(send_data))
            if response and response.text:
                res_json = response.json()
                if res_json['response_code'] == 0:
                    print("发送文章成功")
                else:
                    print(f"发送文章失败：{res_json}")
            else:
                print("发送文章失败：请求失败")
        except Exception as e:
            print(f"发送文章失败：{e}")
    
    def run(self):
        """
        每日登录 +10成长值
        """
        try:
            my_info = self.get_my_info()
            if not my_info:
                print("Threatbook 登录失败")
            else:
                print(f"Threatbook 登录成功, 您的账号：{my_info.get('nickName')}")
                total_point, details_str = self.get_point_info()
                # 检查是否需要获取数据
                need_like = '内容点赞×10' not in details_str
                need_follow = '关注创作者×3' not in details_str

                if need_like and need_follow:
                    # 只在同时需要点赞和关注时获取数据
                    article_data_list, like_list, follow_list = self.get_article_data()
                    
                    # 处理点赞
                    if len(like_list) != 0:
                        self.like(like_list)
                    
                    # 处理关注
                    if len(follow_list) != 0:
                        self.follow(follow_list)
                else:
                    # 单独处理点赞任务
                    if need_like:
                        _, like_list, _ = self.get_article_data()
                        if len(like_list) != 0:
                            self.like(like_list)
                    else:
                        print('今日内容点赞已达上限，中止点赞')
                    
                    # 单独处理关注任务
                    if need_follow:
                        _, _, follow_list = self.get_article_data()
                        if len(follow_list) != 0:
                            self.follow(follow_list)
                    else:
                        print('今日关注创作者已达上限，中止关注')

                print('任务完成！')
                print('-----------------------------------------------------------------')
                self.get_gradeIntroduction_info()
        except Exception as e:
                print(f"运行失败{e}")

def threatbook_main():
    auto = ThreatbookAuto()
    auto.run()

threatbook_main()