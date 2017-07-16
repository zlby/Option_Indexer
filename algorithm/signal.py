import datetime
import numpy as np
import algorithm.database_link as dl
import time


def operation(interval_a_lt, interval_a_rt, interval_b_lt, interval_b_rt, interval_c_lt, interval_c_rt, option_code_1,
              option_code_2, flag_in):
    # return: benefit_end, the benefit after the operation
    #         flag_out
    current_time = datetime.datetime.now()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    closing_time_yesterday = datetime.datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day, hour=15,
                                               minute=0)
    # print(yesterday)
    # print(current_time)
    # print(closing_time_yesterday)
    # 取出数据库中当前隐含波动率
    vol1 = dl.getvol(option_code_1, current_time)
    vol2 = dl.getvol(option_code_2, current_time)
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


# def calc_cash_deposit(closing_price_yesterday_of_future, closing_price_yesterday_of_option, contracts_for_option,
#                       exercise_price, is_call_option=True):
#     contracts_for_future = 10 * contracts_for_option
#     if is_call_option:
#         out_of_the_money = max(exercise_price - closing_price_yesterday_of_future, 0)
#         cash_deposit_1 = closing_price_yesterday_of_option + closing_price_yesterday_of_future * 0.07 - 0.5 * out_of_the_money
#         cash_deposit_1 *= contracts_for_future
#         cash_deposit_2 = closing_price_yesterday_of_option + 0.5 * closing_price_yesterday_of_future * 0.07
#         cash_deposit_2 *= contracts_for_future
#         cash_deposit_of_option = max(cash_deposit_1, cash_deposit_2)
#         cash_deposit_of_future = closing_price_yesterday_of_future * 0.07 * contracts_for_future
#         return cash_deposit_of_option + cash_deposit_of_future
#     else:
#         out_of_the_money = max(closing_price_yesterday_of_future - exercise_price, 0)
#         cash_deposit_1 = closing_price_yesterday_of_option + closing_price_yesterday_of_future * 0.07 - 0.5 * out_of_the_money
#         cash_deposit_1 *= contracts_for_future
#         cash_deposit_2 = closing_price_yesterday_of_option + 0.5 * closing_price_yesterday_of_future * 0.07
#         cash_deposit_2 *= contracts_for_future
#         cash_deposit_of_option = max(cash_deposit_1, cash_deposit_2)
#         cash_deposit_of_future = closing_price_yesterday_of_future * 0.07 * contracts_for_future
#         return cash_deposit_of_option + cash_deposit_of_future


# operation(1, 1, 1, 1, 1, 1, 1, 1)

def remind_customer(option_code_1, option_code_2, interval_a_lt, interval_a_rt, interval_b_lt, interval_b_rt,
                    interval_c_lt, interval_c_rt):
    # benefit = 0
    flag = False
    while (True):
        time_start = datetime.datetime.now()
        flag = operation(interval_a_lt, interval_a_rt, interval_b_lt, interval_b_rt, interval_c_lt,
                         interval_c_rt, option_code_1, option_code_2, flag)
        # print('function end')
        time_end = datetime.datetime.now()
        time_period = time_end - time_start
        time_seconds = time_period.seconds
        time.sleep(60 - time_seconds)


# if __name__ == '__main__':
    # remind_customer(1, 1, 1, 1, 1, 1, 1, 1)


