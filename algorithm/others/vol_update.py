# import tensorflow as tf
# import numpy as np
# import pymysql.cursors
# from algorithm.implied_volatility import *
# import datetime

# config = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'password': '',
#     'db': 'option',
#     'charset': 'utf8mb4',
#     'cursorclass': pymysql.cursors.DictCursor,
# }
#
# info = []
#
#
# # m1709 终止日期是9/14
#
#
# def calculate_vol(code, time, final_time):
#     connection = pymysql.connect(**config)
#     try:
#         # connection = pymysql.connect(**config)
#         with connection.cursor() as cursor:
#             sql = "select time, open from " + code + " where time=%s"
#             cursor.execute(sql, (time,))
#             result = cursor.fetchone()
#             info.append(result["time"])
#             info.append(result["open"])
#         connection.commit()
#     finally:
#         connection.close()
#
#     connection = pymysql.connect(**config)
#     try:
#         # connection = pymysql.connect(**config)
#         with connection.cursor() as cursor:
#             sql = "select time, open from option_minute_test where time = %s"
#             cursor.execute(sql, (time))
#             result = cursor.fetchone()
#             info.append(result["open"])
#         connection.commit()
#     finally:
#         connection.close()
#
#     t = (final_time - time).days
#     # print(info[1])
#     # print(info[2])
#     v = Volatility(info[1], info[2], r=0.015, t=t / 252, k=2500)
#     result = v.get_result()
#     return result
#
#
# if __name__ == '__main__':
#     # time = datetime.datetime(2017, 5, 16, 10, 10, 00)
#     final_time = datetime.datetime(2017, 9, 14)
#     # print(time)
#     # print(calculate_vol("m1709c2500", time=time, final_time=final_time))
#     time_list = []
#     connection = pymysql.connect(**config)
#     try:
#         with connection.cursor() as cursor:
#             sql = "select time from option_minute_test where time>=%s"
#             cursor.execute(sql, (datetime.datetime(2017, 4, 6),))
#             time_list = cursor.fetchall()
#             sql_update = "update m1709c2600 set vol=%s where time=%s"
#             for times in time_list:
#                 vol_value = calculate_vol("m1709c2600", times['time'], final_time)
#                 cursor.execute(sql_update, (str(vol_value), times['time']))
#             connection.commit()
#     finally:
#         connection.close()
#         print("complete")
#
#         # for time in time_list:
#         #     # print(time_list[0]['time'])
#         #     vol_value = calculate_vol("m1709c2500", time['time'], final_time)
#         #     print(vol_value)

import warnings
from datetime import datetime

import algorithm.others.database_link as dl

from algorithm.others.implied_volatility import *
from option.models import *

warnings.filterwarnings("ignore")


def cal_vol(code, current_time, final_time):
    future_code = code.split('-')[0]
    agreement_price = int(code.split('-')[-1])
    days = (final_time - current_time).days
    t = days / 252
    # print(t)
    future_price = dl.get_future_price(code=future_code, time=current_time)
    option_price = dl.get_option_price(code=code, time=current_time)
    # v = Volatility(c=option_price, s0=future_price, r=0.015, t=t, k=agreement_price) # 修改
    v = Volatility(c=option_price, s0=future_price, r=0.015, t=t, k=agreement_price)
    result = v.get_result()
    # print(agreement_price)
    return result


def cal_vol_direct(option_code, option_price, future_price, delivery_day):
    agreement_price = int(option_code.split('-')[-1])
    current_day = datetime.today()
    days = (delivery_day - current_day).days
    t = days / 252
    v = Volatility(c=option_price, s0=future_price, r=0.015, t=t, k=agreement_price)
    return v.get_result()




def update_vol():
    option_list = []
    query_set = Option.objects.all()
    for item in query_set:
        option_list.append(item.code)
    for option_code in option_list:
        print(option_code)
        query_option_data = OptionTreadingData.objects.filter(option=option_code)
        current_time_list = []
        future_code = option_code.split("-")[0]
        final_time = Future.objects.get(code=future_code).delivery_day
        # final_time = datetime.datetime()
        final_time = datetime.strptime(str(final_time), '%Y-%m-%d')
        # print(final_time)
        # final_time = final_time.replace(tzinfo=None)
        for ite in query_option_data:
            current_time_list.append(ite.time)
            # print(ite.time)
        for current_time in current_time_list:
            # print(option_code)
            # print(current_time)
            current_time = current_time.replace(tzinfo=None)
            try:
                tup = OptionTreadingData.objects.get(option=option_code, time=current_time)
                vol = cal_vol(option_code, current_time, final_time)
                tup.volatility = vol
                tup.save()
            except:
                print("error")
                print(option_code)
                print(current_time)



    print("complete")

    #
    #
    # if __name__ == '__main__':
    #     t1 = datetime.datetime(2017, 5, 16, 10, 10, 00)
    #     t2 = datetime.datetime(2017, 9, 14)
    #     cal_vol('m1708-c-2500', t1, t2)
