import yaml
import datetime

def calculate_remaining_days(expiration_date):
    current_date = datetime.date.today()
    remaining_days = (expiration_date - current_date).days
    return remaining_days

def print_remaining_days(data_type, data_name, expiration_date, remaining_days):
    if remaining_days == 20 or (remaining_days < 14 and remaining_days > 0):
        print("类型：", data_type)
        print("域名：", data_name)
        print("到期时间：", expiration_date)
        print("剩余天数：", remaining_days)

def calculate_and_print_remaining_days(data_type, data_name, expiration_date):
    remaining_days = calculate_remaining_days(expiration_date)
    print_remaining_days(data_type, data_name, expiration_date, remaining_days)

def renew_main():
    # 加载配置
    push_config = yaml.safe_load(open(r"config/config.yaml", "r", encoding="utf-8").read())

    # 打印到期提醒
    for renewal in push_config['renewals']:
        expiration_date = datetime.datetime.strptime(renewal['expiration_date'], "%Y-%m-%d").date()
        calculate_and_print_remaining_days(renewal['type'], renewal['domain'], expiration_date)

# renew_main()
