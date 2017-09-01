import datetime
import time

import numpy as np

import algorithm.others.database_link as dl
# from datetime import datetime
from option.models import *


def operation(interval_a_lt, interval_a_rt, interval_b_lt, interval_b_rt, interval_c_lt, interval_c_rt, option_code_1,
              option_code_2, flag_in):
    # return: benefit_end, the benefit after the operation
    #         flag_out
    current_time = datetime.datetime.now()
    # 去掉秒
    current_time = datetime.datetime(current_time.year, current_time.month, current_time.day,
                                     current_time.hour, current_time.minute, second=0)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    closing_time_yesterday = datetime.datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day, hour=15,
                                               minute=0)
    # print(yesterday)
    # print(current_time)
    # print(closing_time_yesterday)
    # 取出数据库中当前隐含波动率
    vol1 = dl.get_option_vol(option_code_1, current_time)
    vol2 = dl.get_option_vol(option_code_2, current_time)
    diff = vol1 - vol2
    signal = np.sign(diff)
    flag_out = flag_in

    if False == flag_in:
        if interval_a_lt < diff < interval_a_rt:
            # benefit_end = benefit_start - 10 * dl.getprice(option_code_1, current_time) * signal
            # benefit_end = benefit_end - calc_cash_deposit(dl.getprice(option_code_1, closing_time_yesterday))
            # benefit_end = benefit_end + 10 * dl.getprice(option_code_2, current_time) * signal
            # benefit_end = benefit_end - calc_cash_deposit(dl.getprice(option_code_2, closing_time_yesterday))
            # 买1 卖2  *signal
            # 从数据库中取出所有订阅了code1和code2的用户，然后给他们发消息
            flag_out = True
        elif interval_c_lt < diff < interval_b_lt or interval_b_rt < diff < interval_c_rt:
            # benefit_end = benefit_start + 10 * dl.getprice(option_code_2, current_time) * signal
            # benefit_end = benefit_end - calc_cash_deposit(dl.getprice(option_code_2, closing_time_yesterday))
            # benefit_end = benefit_end - 10 * dl.getprice(option_code_1, current_time) * signal
            # benefit_end = benefit_end - calc_cash_deposit(dl.getprice(option_code_1, closing_time_yesterday))
            # 卖1 买2 *signal
            # 从数据库中取出所有订阅了code1和code2的用户，然后给他们发消息
            flag_out = True
        elif diff < interval_c_lt or diff > interval_c_rt:
            # benefit_end = benefit_start - 10 * dl.getprice(option_code_1, current_time) * signal
            # benefit_end = benefit_end - calc_cash_deposit(dl.getprice(option_code_1, closing_time_yesterday))
            # benefit_end = benefit_end + 10 * dl.getprice(option_code_2, current_time) * signal
            # benefit_end = benefit_end - calc_cash_deposit(dl.getprice(option_code_2, closing_time_yesterday))
            # 买1 卖2 *signal
            # 从数据库中取出所有订阅了code1和code2的用户，然后给他们发消息
            flag_out = True
        else:
            # benefit_end = benefit_start
            flag_out = False
    if True == flag_in:
        if interval_b_lt < diff < interval_a_lt or interval_a_rt < diff < interval_b_rt:
            flag_out = False
            # 提示用户套利机会已消失
            # benefit_end = benefit_start

    return flag_out





def start_remind():
    query_set = Intervals.objects.all()
    flag = []
    for _ in query_set:
        flag.append(False)
    while True:
        time_start = datetime.datetime.now()
        for i in range(len(query_set)):
            item = query_set[i]
            flag[i] = operation(item.lower_bound_a, item.upper_bound_a, item.lower_bound_b, item.upper_bound_b,
                                item.lower_bound_c,
                                item.upper_bound_c, item.positive_option_id, item.negative_option_id, flag[i])

        time_end = datetime.datetime.now()
        time_period = time_end - time_start
        time_seconds = time_period.seconds
        time.sleep(60 - time_seconds)

