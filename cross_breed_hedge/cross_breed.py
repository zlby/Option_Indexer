from option.models import *
from cross_breed_hedge.coherence import *
from cross_breed_hedge.error_diagram import *
import datetime


def show_crop_diagram(type:str):
    query_set = Crop.objects.filter(type=type).order_by('-time')[:300]

    result_set = []
    for item in query_set:
        result_set.insert(0, (item.time, item.price))

    return result_set


def show_future_diagram(code:str):
    query_set = ContinuousDayFutureTreadingData.objects.filter(type=code).order_by('-time')[:300]

    result_set = []

    for item in query_set:
        result_set.insert(0, (item.time, item.close_price))

    return result_set


def choose_futures(type:str, time_future:datetime.datetime = None):
    query_set_crop = Crop.objects.filter(type=type).order_by('-time')[:300]
    result_set = []
    crop_list = []
    for item in query_set_crop:
        crop_list.insert(0, item.price)

    future_type_list = ['豆粕', '棕榈油', '玉米', '玉米淀粉', '纤维板', '胶合板', '豆油', '鸡蛋']

    for type in future_type_list:
        query = ContinuousDayFutureTreadingData.objects.filter(type=type).order_by('-time')[:300]
        if len(query) != 300:
            continue
        future_list = []
        for item in query:
            future_list.insert(0, item.close_price)

        co = abs(get_coherence_rate(crop_list, future_list))
        rate = abs(OLS(diffx=get_diff(future_list), diffy=get_diff(crop_list)))
        result_set.append((type, rate, co))
        result_set.sort(key=lambda co : co[2], reverse=True)
    return result_set


def show_error_diagram(type:str, code:str):
    query_set_crop = Crop.objects.filter(type=type).order_by('-time')[:500]
    crop_list = []
    time_list = []
    for item in query_set_crop:
        crop_list.insert(0, item.price)
        time_list.insert(0, item.time)
    query_set_future = ContinuousDayFutureTreadingData.objects.filter(type=code).order_by('-time')[:500]
    future_list = []
    for item in query_set_future:
        future_list.insert(0, item.close_price)

    return show_diagram(crop_list, future_list, time_list)

