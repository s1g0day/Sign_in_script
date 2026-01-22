#Filename: fish_reminder.py
#Author: s1g0day
#Date: 2025/02/27
#Update: 2025/12/29
#Description: 摸鱼提醒


from datetime import date, timedelta, datetime
from lunar_python import Lunar, Solar
from lib.logger_init import logger
# from modules.threatbook.threatbook import ThreatbookAuto

class FishReminder:
    def __init__(self):
        self.today = date.today()
        # self.today = date(2025, 4, 5)
        self.weekday = self.today.weekday()
        self.year_start = date(self.today.year, 1, 1)
        self.days_passed = (self.today - self.year_start).days
        
    def get_weekend_countdown(self):
        days_to_saturday = (5 - self.weekday) % 7 or 7
        days_to_sunday = (6 - self.weekday) % 7 or 7
        return days_to_saturday, days_to_sunday
        
    def get_payday_countdown(self):
        pay_days = [1, 5, 10, 15, 20]
        countdowns = {}
        for day in pay_days:
            if self.today.day <= day:
                target = date(self.today.year, self.today.month, day)
            else:
                next_month = self.today.month + 1 if self.today.month < 12 else 1
                year = self.today.year if next_month > 1 else self.today.year + 1
                target = date(year, next_month, day)
            countdowns[f"{day}号发工资"] = (target - self.today).days
        # Add month-end payday
        next_month = self.today.month + 1 if self.today.month < 12 else 1
        year = self.today.year if next_month > 1 else self.today.year + 1
        month_end = date(year, next_month, 1) - timedelta(days=1)
        countdowns["月底发工资"] = (month_end - self.today).days
        return countdowns
        
    def get_holiday_countdown(self):
        current_year = self.today.year
        next_year = current_year + 1
        
        # 获取农历节日日期
        def get_lunar_holiday(year, lunar_month, lunar_day):
            try:
                lunar = Lunar.fromYmd(year, lunar_month, lunar_day)
                solar = lunar.getSolar()
                return date(solar.getYear(), solar.getMonth(), solar.getDay())
            except Exception:
                # 如果是除夕，找到当月最后一天
                if lunar_month == 12 and lunar_day == 30:
                    try:
                        lunar = Lunar.fromYmd(year, lunar_month, 29)
                        solar = lunar.getSolar()
                        return date(solar.getYear(), solar.getMonth(), solar.getDay())
                    except Exception:
                        return None
                return None

        # 定义节假日规则
        holiday_rules = [
            {"name": "元旦", "type": "solar", "month": 1, "day": 1, "days": 3},
            {"name": "春节", "type": "lunar", "month": 1, "day": 1, "days": 7},
            {"name": "清明节", "type": "solar", "month": 4, "day": 5, "days": 3},
            {"name": "劳动节", "type": "solar", "month": 5, "day": 1, "days": 5},
            {"name": "端午节", "type": "lunar", "month": 5, "day": 5, "days": 3},
            {"name": "中秋节", "type": "lunar", "month": 8, "day": 15, "days": 3},
            {"name": "国庆节", "type": "solar", "month": 10, "day": 1, "days": 7}
        ]
        
        result = {}
        for rule in holiday_rules:
            name = rule["name"]
            days = rule["days"]
            
            # 计算今年的节日日期
            if rule["type"] == "solar":
                holiday_date = date(current_year, rule["month"], rule["day"])
            else:
                holiday_date = get_lunar_holiday(current_year, rule["month"], rule["day"])
            
            if holiday_date is None:
                continue

            # 如果今年已过，计算明年的日期
            if holiday_date < self.today:
                if rule["type"] == "solar":
                    holiday_date = date(next_year, rule["month"], rule["day"])
                else:
                    holiday_date = get_lunar_holiday(next_year, rule["month"], rule["day"])
            
            if holiday_date:
                solar = Solar(holiday_date.year, holiday_date.month, holiday_date.day, 0, 0, 0)
                lunar = solar.getLunar()
                lunar_str = f"{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
                result[f"{name}{'(%d天)' % days if days > 0 else ''} [{holiday_date.year}-{holiday_date.month}-{holiday_date.day} 农:{lunar_str}]"] = (holiday_date, days)
                
        return {name: (d - self.today).days for name, (d, _) in result.items()}

    def get_thursday_countdown(self):
        # 计算下一个星期四
        days_until_thursday = (3 - self.weekday) % 7  # 3代表星期四
        next_thursday = self.today + timedelta(days=days_until_thursday)
        return (next_thursday - self.today).days
    
    def generate_message(self):
        # 疯狂星期四倒计时
        thursday = self.get_thursday_countdown()
        
        # 周末倒计时
        sat, sun = self.get_weekend_countdown()
        
        # 工资倒计时
        paydays = self.get_payday_countdown()
        
        # 节假日倒计时
        holidays = self.get_holiday_countdown()
        
        week_days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        current_weekday = week_days[self.weekday]

        # 检查特殊日子
        special_days = []
        if thursday == 0:
            special_days.append("今天是疯狂星期四！")
        if sat == 0:
            special_days.append("今天是周六！")
        if sun == 0:
            special_days.append("今天是周日！")
        for name, days in paydays.items():
            if days == 0:
                special_days.append(f"今天是{name}！")
        for name, days in holidays.items():
            if days == 0:
                special_days.append(f"今天是{name}！")

        # 获取当前农历日期
        current_solar = Solar(self.today.year, self.today.month, self.today.day, 0, 0, 0)
        current_lunar = current_solar.getLunar()
        lunar_str = f"{current_lunar.getYearInChinese()}年 {current_lunar.getMonthInChinese()}月{current_lunar.getDayInChinese()}"
        
        # 计算当前是第几周
        first_day = date(self.today.year, 1, 1)
        week_number = (self.today - first_day).days // 7 + 1

        special_reminder = "🎉 " + " ".join(special_days) if special_days else ""

        # 添加休息日和节日提醒
        today_special = ""
        if self.weekday >= 5:  # 周六或周日
            today_special = f"⏰ 今天是{current_weekday}，休息日请好好放松哦！\n\n"
        
        # 检查今天是否是节日
        today_holiday = None
        for name, days in holidays.items():
            if days == 0:
                holiday_name = name.split(" [")[0].split("(")[0]  # 去掉日期部分和天数
                today_special = f"🎊 今天是{holiday_name}，{'休息日' if '(' in name else '节假日'}，祝您节日快乐！\n\n"
                break

        message = f"""【摸鱼办】提醒您：现在时间是{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}，
第{week_number}周，农历{lunar_str}，{current_weekday} {special_reminder}😜

{today_special}{self.today.year} 年已经过去 {self.days_passed} 天 ⌛️！
你好，摸鱼人！👨‍💻 工作再忙，一定不要忘记摸鱼哦 🐟！
有事没事起身去茶水间 ☕️，去厕所 🚾，去走廊走走 🚶，去找同事聊聊八卦 🆕！别老在工位上坐着，钱是老板的 👨‍💼 但命是自己的 🤷‍♂️。

🥳 疯狂星期四
距离【疯狂星期四】还有 {thursday} 天

🥳 周末
距离【周六】还有 {sat} 天
距离【周日】还有 {sun} 天

💴 工资
"""
        for name, days in paydays.items():
            message += f"距离【{name}】还有 {days} 天\n"
            
        message += "\n🎉 节假日\n"
        # 按照日期排序节假日
        sorted_holidays = sorted(holidays.items(), key=lambda x: x[1])
        for name, days in sorted_holidays:
            message += f"距离【{name}】还有 {days} 天\n"
            
        return message

# 判断现在时间是否是在8点到18点之间
def is_working_time():
    now = datetime.now()
    if 8 <= now.hour < 18:
        return True

def fishReminder_main():
    reminder = FishReminder()
    message = reminder.generate_message()  # Get the generated message
    logger.info(message)
    print(message)
    # auto = ThreatbookAuto()
    # if is_working_time():      
    #     # auto.fish_reminder_send_article(message)
    #     logger.info("测试")
    #     print("测试")
    # else:
    #     logger.info("当前时间不在工作时间，不发送消息")
    #     print("当前时间不在工作时间，不发送消息")
    # return message