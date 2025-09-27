import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 日志目录
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'sign.log')

# 日志格式
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# TimedRotatingFileHandler: 每周一0点分割，保留4周
file_handler = TimedRotatingFileHandler(log_file, when='W0', interval=1, backupCount=4, encoding='utf-8')
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 获取logger
logger = logging.getLogger('sign_logger')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.propagate = False
