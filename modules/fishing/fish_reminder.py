#Filename: fish_reminder.py
#Author: s1g0day
#Date: 2025/02/27
#Update: 2025/05/12
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

        # 定义节假日及放假天数
        holidays = {
            "元旦": (date(current_year, 1, 1), 3),
            "春节": (get_lunar_holiday(current_year, 1, 1), 7),     # 农历正月初一
            "清明节": (date(current_year, 4, 5), 3),
            "劳动节": (date(current_year, 5, 1), 5),
            "端午节": (get_lunar_holiday(current_year, 5, 5), 3),   # 农历五月初五
            "中秋节": (get_lunar_holiday(current_year, 8, 15), 3),  # 农历八月十五
            "国庆节": (date(current_year, 10, 1), 7),
            "元旦": (date(next_year, 1, 1), 3)
        }
        
        # 如果当前日期已过，则使用下一年的日期
        result = {}
        for name, (holiday_date, days) in holidays.items():
            if holiday_date is None:
                continue
            if holiday_date < self.today:
                if isinstance(holiday_date, date):
                    # 公历节日
                    new_date = date(next_year, holiday_date.month, holiday_date.day)
                    solar = Solar(new_date.year, new_date.month, new_date.day, 0, 0, 0)
                    lunar = solar.getLunar()
                    lunar_str = f"{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
                else:
                    # 农历节日
                    lunar_date = Lunar.fromDate(holiday_date)
                    new_date = get_lunar_holiday(next_year, lunar_date.getMonth(), lunar_date.getDay())
                    solar = Solar(new_date.year, new_date.month, new_date.day, 0, 0, 0)
                    lunar = solar.getLunar()
                    lunar_str = f"{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
                result[f"{name}{'(放假%d天)' % days if days > 0 else ''} [阳历：{new_date.month}月{new_date.day}日 农历：{lunar_str}]"] = (new_date, days)
            else:
                solar = Solar(holiday_date.year, holiday_date.month, holiday_date.day, 0, 0, 0)
                lunar = solar.getLunar()
                lunar_str = f"{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
                result[f"{name}{'(放假%d天)' % days if days > 0 else ''} [阳历：{holiday_date.month}月{holiday_date.day}日 农历：{lunar_str}]"] = (holiday_date, days)
                
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
                holiday_name = name.split(" [")[0]  # 去掉日期部分
                today_special = f"🎊 今天是{holiday_name}，{'休息日' if '(放假' in name else '节假日'}，祝您节日快乐！\n\n"
                break

        message = f"""【摸鱼办】提醒您：现在时间是{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}，
第{week_number}周，农历{lunar_str}，{current_weekday} {special_reminder}😜

{today_special}2025 年已经过去 {self.days_passed} 天 ⌛️！
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
    if 8 <= now.hour < 10:
        return True

def fishReminder_main():
    # auto = ThreatbookAuto()
    reminder = FishReminder()
    message = reminder.generate_message()  # Get the generated message
    logger.info(message)
    print(message)
    if is_working_time():      
        # auto.fish_reminder_send_article(message)
        logger.info("测试")
        print("测试")
    else:
        logger.info("当前时间不在工作时间，不发送消息")
        print("当前时间不在工作时间，不发送消息")
    return message