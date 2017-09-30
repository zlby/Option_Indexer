from option.models import *
from cross_breed_hedge.coherence import *
from cross_breed_hedge.error_diagram import *
import datetime

def show_crop_diagram(type:str):
    query_set = Crop.objects.filter(type=type).order_by('-time')[:500]

    result_set = []
    for item in query_set:
        result_set.insert(0, (item.time, item.price))

    return result_set

def show_future_diagram(code:str):
    query_set = DayFutureTreadingData.objects.filter(future=code).order_by('-time')[:500]

    result_set = []

    for item in query_set:
        result_set.insert(0, (item.time, item.close_price))

    return result_set

def choose_futures(type:str, time_future:datetime.datetime):
    query_set_crop = Crop.objects.filter(type=type).order_by('-time')[:500]
    result_set = []
    crop_list = []
    for item in query_set_crop:
        crop_list.insert(0, item.price)

    query_set_future = ContinuousDayFutureTreadingData.objects.all()
    future_code_list = []
    for item in query_set_future:
        future_code_list.append(item.code)

    for code in future_code_list:
        query = FutureTreadingData.objects.filter(future=code).order_by('-time')[:500]
        if len(query) != 500:
            continue
        future_list = []
        for item in query:
            future_list.insert(0, item.close_price)

        co = abs(get_coherence_rate(crop_list, future_list))
        rate = abs(OLS(diffx=get_diff(future_list), diffy=get_diff(crop_list)))
        result_set.append((code, rate, co))
        result_set.sort(key=lambda co : co[1], reverse=True)
    return result_set


def show_error_diagram(type:str, code:str):
    query_set_crop = Crop.objects.filter(type=type).order_by('-time')[:500]
    crop_list = []
    time_list = []
    for item in query_set_crop:
        crop_list.insert(0, item.price)
        time_list.insert(0, item.time)
    query_set_future = FutureTreadingData.objects.filter(future=code).order_by('-time')[:500]
    future_list = []
    for item in query_set_future:
        future_list.insert(0, item.close_price)

    return show_diagram(crop_list, future_list, time_list)

