import time
from datetime import datetime
from loguru import logger


def setup_logger():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    logger.add(f'logs/log_{timestamp}.log', level='DEBUG')

    # logger.add('logs/log.log', rotation='1 day', level='DEBUG')

    return logger


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n ⏳ The vulnerability scanner ran for {round(end_time - start_time, 2)} seconds")
        return result

    return wrapper
