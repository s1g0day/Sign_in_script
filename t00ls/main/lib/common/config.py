
# coding:utf-8
def config():
    push_config = {
        'domain': "https://www.t00ls.com",
        'uname': 'uname',  # 帐号
        'pswd': 'pswd',  # 密码
        'qesnum': 1,  # 安全提问 参考下面
        'qan': 'qan',  # 安全提问答案

        # 0 = 没有安全提问
        # 1 = 母亲的名字
        # 2 = 爷爷的名字
        # 3 = 父亲出生的城市
        # 4 = 您其中一位老师的名字
        # 5 = 您个人计算机的型号
        # 6 = 您最喜欢的餐馆名称
        # 7 = 驾驶执照的最后四位数字
    } 

    return push_config