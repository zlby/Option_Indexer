from option.models import *
import datetime as dt
import warnings

warnings.filterwarnings('ignore')


def save_data_transfered_option(time_begin, time_end, timedelta: dt.timedelta, shift_timedelta):
    data_object_list = []

    query_set = Option.objects.all()
    for item in query_set:
        print(item.code)
        time_iter = time_begin
        while time_iter < time_end:
            data_list = OptionTreadingData.objects.filter(time__range=(time_iter, time_iter + timedelta),
                                                          option=item.code).order_by('time')
            # print(time_iter)
            # print(time_iter + timedelta)

            if data_list.count() > 0:
                # print(data_list.count())
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


                if timedelta.days == 1:
                    data_object_list.append(
                        DayOptionTreadingData(time=time_iter + shift_timedelta, open_price=new_open_price,
                                               close_price=new_close_price, max_price=new_max_price,
                                               min_price=new_min_price, volatility=new_volatility, volume=new_volume,
                                               option=Option(code=item.code)))
                else:
                    data_object_list.append(
                        HourOptionTreadingData(time=time_iter + shift_timedelta, open_price=new_open_price,
                                              close_price=new_close_price, max_price=new_max_price,
                                              min_price=new_min_price, volatility=new_volatility, volume=new_volume,
                                              option=Option(code=item.code)))
                if len(data_object_list) > 1000:
                    if timedelta.days == 1:
                        DayOptionTreadingData.objects.bulk_create(data_object_list)
                    else:
                        HourOptionTreadingData.objects.bulk_create(data_object_list)
                    data_object_list = []

            time_iter += timedelta
            # print(len(data_object_list))

    if timedelta.days == 1:
        DayOptionTreadingData.objects.bulk_create(data_object_list)
    else:
        HourOptionTreadingData.objects.bulk_create(data_object_list)


def save_data_transfered_future(time_begin, time_end, timedelta:dt.timedelta, shift_timedelta):
    data_object_list = []

    query_set = Future.objects.all()
    for item in query_set:
        print(item.code)
        time_iter = time_begin
        while time_iter < time_end:
            data_list = FutureTreadingData.objects.filter(time__range=(time_iter, time_iter + timedelta),
                                                          future=item.code).order_by('time')
            # print(time_iter)
            # print(time_iter + timedelta)

            if data_list.count() > 0:
                # print(data_list.count())
                new_open_price = data_list[0].open_price
                new_close_price = data_list[len(data_list) - 1].close_price
                # new_volatility = data_list[len(data_list) - 1].volatility
                # new_volume = 0
                new_max_price = 0
                new_min_price = 100000
                for data in data_list:
                    new_max_price = data.close_price if data.close_price > new_max_price else new_max_price
                    new_min_price = data.close_price if data.min_price < new_min_price else new_min_price
                    # new_volume += data.volume
                if timedelta.days == 1:
                    data_object_list.append(
                        DayFutureTreadingData(time=time_iter + shift_timedelta, open_price=new_open_price,
                                               close_price=new_close_price, max_price=new_max_price,
                                               min_price=new_min_price,# volatility=new_volatility, volume=new_volume,
                                               future=Future(code=item.code)))
                else:
                    data_object_list.append(
                        HourFutureTreadingData(time=time_iter + shift_timedelta, open_price=new_open_price,
                                               close_price=new_close_price, max_price=new_max_price,
                                               min_price=new_min_price,  # volatility=new_volatility, volume=new_volume,
                                               future=Future(code=item.code)))
                if len(data_object_list) > 1000:
                    if timedelta.days == 1:
                        DayFutureTreadingData.objects.bulk_create(data_object_list)
                    else:
                        HourFutureTreadingData.objects.bulk_create(data_object_list)
                    data_object_list = []

            time_iter += timedelta
            # print(len(data_object_list))
    if timedelta.days == 1:
        DayFutureTreadingData.objects.bulk_create(data_object_list)
    else:
        HourFutureTreadingData.objects.bulk_create(data_object_list)

