from option.models import *
import datetime as dt


def save_data_transfered(time_begin, time_end, timedelta, shift_timedelta):
    data_object_list = []

    query_set = Option.objects.all()
    for item in query_set:
        print(item.code)
        time_iter = time_begin
        while time_iter < time_end:
            data_list = OptionTreadingData.objects.filter(time__range=(time_iter, time_iter + timedelta),
                                                          option=item.code)
            if data_list.count() > 0:
                new_open_price = data_list[0].open_price
                new_close_price = data_list[len(data_list) - 1].close_price
                new_volatility = data_list[len(data_list) - 1].volatility
                new_volume = 0
                new_max_price = 0
                new_min_price = 100000
                for data in data_list:
                    new_max_price = data.close_price if data.close_price > new_max_price else new_max_price
                    new_min_price = data.close_price if data.min_price < new_min_price else new_min_price
                    new_volume += data.volume
                data_object_list.append(
                    DayOptionTreadingData(time=time_iter + shift_timedelta, open_price=new_open_price,
                                          close_price=new_close_price, max_price=new_max_price,
                                          min_price=new_min_price, volatility=new_volatility, option=Option(code=item.code),
                                          volume=new_volume))

            time_iter += timedelta

        DayOptionTreadingData.objects.bulk_create(data_object_list)
