import csv
# from django.db import models
from option.models import *


def calc_cash_deposit(closing_price_yesterday_of_future, closing_price_yesterday_of_option, contracts_for_option,
                      exercise_price, is_call_option=True):
    contracts_for_future = 10 * contracts_for_option
    if is_call_option:
        out_of_the_money = max(exercise_price - closing_price_yesterday_of_future, 0)
        cash_deposit_1 = closing_price_yesterday_of_option + closing_price_yesterday_of_future * 0.07 - 0.5 * out_of_the_money
        cash_deposit_1 *= contracts_for_future
        cash_deposit_2 = closing_price_yesterday_of_option + 0.5 * closing_price_yesterday_of_future * 0.07
        cash_deposit_2 *= contracts_for_future
        cash_deposit_of_option = max(cash_deposit_1, cash_deposit_2)
        cash_deposit_of_future = closing_price_yesterday_of_future * 0.07 * contracts_for_future
        return cash_deposit_of_option + cash_deposit_of_future
    else:
        out_of_the_money = max(closing_price_yesterday_of_future - exercise_price, 0)
        cash_deposit_1 = closing_price_yesterday_of_option + closing_price_yesterday_of_future * 0.07 - 0.5 * out_of_the_money
        cash_deposit_1 *= contracts_for_future
        cash_deposit_2 = closing_price_yesterday_of_option + 0.5 * closing_price_yesterday_of_future * 0.07
        cash_deposit_2 *= contracts_for_future
        cash_deposit_of_option = max(cash_deposit_1, cash_deposit_2)
        cash_deposit_of_future = closing_price_yesterday_of_future * 0.07 * contracts_for_future
        return cash_deposit_of_option + cash_deposit_of_future


def get_option_vol(code, time):
    # get implied volatility for an option
    try:
        res_tuple = OptionTreadingData.objects.get(option=code, time=time)
        return res_tuple.volatility
    except:
        return None
        # if res_tuple is not None:
        #     return res_tuple.volatility
        # else:
        #     return None


def get_option_price(code, time):
    # get price of an opiton
    try:
        res_tuple = OptionTreadingData.objects.get(option=code, time=time)
        return res_tuple.close_price
    except:
        return None


def get_future_price(code, time):
    # get price of an future
    try:
        res_tuple = FutureTreadingData.objects.get(future=code, time=time)
        return res_tuple.close_price
    except:
        return None


        # if __name__ == '__main__':
        #     import os
        #
        #     os.environ['DJANGO_SETTINGS_MODULE'] = 'huaqi.settings'
        #     print(getvol())


# def db_insert():

def get_option_rate_list(code):
    try:
        temp_list = []
        res_list = []
        res_tuples = OptionTreadingData.objects.filter(option=code).order_by('-time')[:2000]
        for i in range(len(res_tuples)):
            temp_list.append(res_tuples[i].volatility)
            # print(res_tuples[i].volatility)
        for i in range(len(temp_list)):
            res_list.append(temp_list[len(temp_list) - i - 1])
        return res_list
    except:
        return None


def get_option_price_list(code):
    try:
        temp_list = []
        res_list = []
        res_tuples = OptionTreadingData.objects.filter(option=code).order_by('-time')[:2000]
        for i in range(len(res_tuples)):
            temp_list.append(res_tuples[i].close_price)
        for i in range(len(temp_list)):
            res_list.append(temp_list[len(temp_list) - i - 1])
        return res_list
    except:
        return None
