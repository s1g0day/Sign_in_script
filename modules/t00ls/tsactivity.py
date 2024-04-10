import re
import requests

def tsactivity_main(s, domain):

    try:
        rurl = domain + '/members-profile.html'
        rsign = s.get(url=rurl)
        rsign.raise_for_status()  # 检查请求是否成功
        signbtn_datas = re.findall(r'disabled value="(.+?)"></h2>', rsign.text)
        activity_datas = re.findall(r'alt="(.+?)"', rsign.text)
        
        # 模糊匹配
        signbtn_search_string = '已签到'
        signbtn_matching_elements = [element for element in signbtn_datas if signbtn_search_string in element]

        if signbtn_matching_elements:
            print("签到天数: " + signbtn_datas[0])
        else:
            print("未找到签到天数数据")

        # 模糊匹配
        activity_search_string = '活跃度'
        activity_matching_elements = [element for element in activity_datas if activity_search_string in element]

        if activity_matching_elements:
            print("活跃等级: " + activity_datas[1] + "\n")
        else:
            print("未找到活跃等级数据")

    
    except requests.exceptions.RequestException as e:
        print("tsactivity_main 请求异常:", e)
    except (IndexError, KeyError) as e:
        print("tsactivity_main 数据提取异常:", e)