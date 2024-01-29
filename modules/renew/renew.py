import datetime

def calculate_remaining_days(expiration_date):
    current_date = datetime.date.today()
    remaining_days = (expiration_date - current_date).days
    return remaining_days

def print_remaining_days(data_type, data_name, expiration_date, remaining_days):
    if remaining_days == 30 or (remaining_days < 7 and remaining_days > 0):
        print("类型：", data_type)
        print("域名：", data_name)
        print("到期时间：", expiration_date)
        print("剩余天数：", remaining_days)

def calculate_and_print_remaining_days(data_type, data_name, expiration_date):
    remaining_days = calculate_remaining_days(expiration_date)
    print_remaining_days(data_type, data_name, expiration_date, remaining_days)

def renew_main():
    datas = [
        {"type": "VPS", "name": "`https://cloud.tencent.com/`", "expiration_date": datetime.date(2024, 11, 18)},
        {"type": "VPS", "name": "`https://cloud.tencent.com/`", "expiration_date": datetime.date(2024, 5, 21)},
        {"type": "VPS", "name": "`https://cloud.tencent.com/`", "expiration_date": datetime.date(2024, 6, 15)},
        {"type": "VPS", "name": "`https://cloud.tencent.com/`", "expiration_date": datetime.date(2024, 6, 14)},
        {"type": "VPS", "name": "`https://cloud.tencent.com/`", "expiration_date": datetime.date(2024, 5, 18)},
        {"type": "VPS", "name": "`https://cloud.tencent.com/`", "expiration_date": datetime.date(2026, 8, 26)},
        {"type": "Domain", "name": "`https://www.namesilo.com/`", "expiration_date": datetime.date(2024, 4, 24)},
        {"type": "voice", "name": "`https://voice.google.com/`", "expiration_date": datetime.date(2024, 12, 1)},
    ]

    for data in datas:
        calculate_and_print_remaining_days(data["type"], data["name"], data["expiration_date"])
# renew_main()
