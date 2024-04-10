import yaml
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
    # 加载配置
    push_config = yaml.safe_load(open(r"config/config.yaml", "r", encoding="utf-8").read())
    login_list = []
    for key in push_config:
        if key.startswith('renew_domain'):
            index = key.split('renew_domain')[1]
            type = push_config['renew_type']
            domain = push_config['renew_domain' + index]
            expiration_date = push_config['renew_expiration_date' + index]
            login_list.append({
                'renew_type': type,
                'renew_domain': domain,
                'renew_expiration_date': expiration_date
            })
    for data in login_list:
        expiration_date = datetime.datetime.strptime(data["renew_expiration_date"], "%Y-%m-%d").date()
        calculate_and_print_remaining_days(data["renew_type"], data["renew_domain"], expiration_date)

# renew_main()
