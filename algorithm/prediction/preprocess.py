r"""Unknown Module
"""

# todo:Complete docString
from option.models import *
import datetime


def data_preprocess(code: str, end_day: datetime.date, days: int):
    start_day = end_day - datetime.timedelta(days=days)
    query_set = FutureTreadingData.objects.filter(future=code).filter(time__gt=start_day).filter(
        time__lt=end_day).order_by('time')
    time_list = []
    close_price = 0
    open_price = 0
    max_price_list = []
    min_price_list = []
    avg_price_list = []
    blurry_data_list = []

    for i in range(days):
        current_day = start_day + datetime.timedelta(days=i)
        sub_query_set = query_set.filter(time__gt=current_day).filter(
            time__lt=(current_day + datetime.timedelta(days=1)))
        day_list = []
        blurry_data_list_day = []
        max_price = 0
        min_price = 100000
        total_price = 0
        for item in sub_query_set:
            day_list.append(item.close_price)
            max_price = item.close_price if close_price > max_price else max_price
            min_price = item.close_price if close_price < min_price else min_price
            total_price += item.close_price
        avg_price = total_price / len(sub_query_set)

        for piece in day_list:
            blurry_data = 0
            if piece < min_price:
                blurry_data = 0
            elif min_price < piece < max_price:
                blurry_data = 0
            elif min_price < piece < avg_price:
                blurry_data = (piece - min_price) / (avg_price - piece)
            elif avg_price < piece < max_price:
                blurry_data = (max_price - piece) / (max_price - avg_price)
            elif piece > max_price:
                blurry_data = 0
            blurry_data_list_day.append(blurry_data)

        max_data = 0
        min_data = 100000
        total_data = 0
        avg_data = 0
        for data in blurry_data_list_day:
            max_data = data if data > max_data else max_data

