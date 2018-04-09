import time


def get_current_timestamp():
    return time.time()


def decode_time_for_human(int_date):
    try:
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(int_date)))
    except TypeError:
        date = 0
        print('Wrong data type. Should be int')
    return date
