# -*- coding: utf-8 -*-
import datetime
import time
import copy
import os
import codecs
from option.models import FutureTreadingData, OptionTreadingData, Future, Option, Spot,  ContinuousDayFutureTreadingData


class FutureTD:
    def __init__(self, f_time, f_open, f_max, f_min, f_close):
        self.future_code = ""
        self.f_time = f_time
        self.f_open = f_open
        self.f_max = f_max
        self.f_min = f_min
        self.f_close = f_close

    def set_future_code(self, future_code):
        self.future_code = future_code

    def set_f_time(self, f_time):
        self.f_time = f_time

    def save(self):
        pass

    def __str__(self):
        return self.f_time.strftime("%Y/%m/%d %H:%M") + "," + \
               self.f_open + "," + \
               self.f_max + "," + \
               self.f_min + "," + \
               self.f_close


def data_transfer(rootdir):
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            print(filename)
            # filename = "m1709-c-2800.csv"
            if "-" not in filename:
                with open(rootdir+"/"+filename, 'r') as f:
                    data_list = f.read().split('\n')
                    data_list = data_list[1:-3]
                    iterator = 0

                    first_row_data = data_list[iterator].split(',')
                    try:
                        first_row_time = datetime.datetime(*(time.strptime(first_row_data[0], "%Y/%m/%d %H:%M")[:6]))
                    except:
                        first_row_time = datetime.datetime(*(time.strptime(first_row_data[0], "%Y-%m-%d %H:%M")[:6]))
                    iterate_time = first_row_time

                    future_threading_groups = []

                    future_for_treading_data = Future.objects.get(code=filename.split('.')[0])
                    # future_for_treading_data.save()

                    while iterator != len(data_list):
                        try:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_list[iterator].split(' ')[0], "%Y/%m/%d"))[:6])
                        except:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_list[iterator].split(' ')[0], "%Y-%m-%d"))[:6])

                        time1_start = begin_date + datetime.timedelta(hours=8, minutes=55)
                        time1_end = begin_date + datetime.timedelta(hours=11, minutes=35)
                        time2_start = begin_date + datetime.timedelta(hours=13, minutes=25)
                        time2_end = begin_date + datetime.timedelta(hours=15, minutes=5)
                        time3_start = begin_date + datetime.timedelta(hours=20, minutes=55)
                        time3_end = begin_date + datetime.timedelta(hours=23, minutes=35)

                        if not (time1_start <= iterate_time <= time1_end or time2_start <= iterate_time <= time2_end or time3_start <= iterate_time <= time3_end):
                            iterator += 1

                        if iterator != 0:
                            iterate_time = time1_start


                        while time1_start <= iterate_time <= time1_end or time2_start <= iterate_time <= time2_end or time3_start <= iterate_time <= time3_end:
                            if iterator == len(data_list):
                                break
                            try:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_list[iterator].split(',')[0],
                                                    "%Y/%m/%d %H:%M")[:6]))
                            except:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_list[iterator].split(',')[0],
                                                    "%Y-%m-%d %H:%M")[:6]))
                            if not ((time1_start <= next_time <= time1_end)
                                or (time2_start <= next_time <= time2_end)
                                or (time3_start <= next_time <= time3_end)):
                                iterator += 1
                                break
                            if iterate_time == next_time:
                                future = FutureTreadingData(time=iterate_time,
                                                            open_price=data_list[iterator].split(',')[1],
                                                            max_price=data_list[iterator].split(',')[2],
                                                            min_price=data_list[iterator].split(',')[3],
                                                            close_price=data_list[iterator].split(',')[4],
                                                            future=future_for_treading_data)
                                future_threading_groups.append(future)
                                iterator += 1
                            else:
                                future = copy.deepcopy(future_threading_groups[-1])
                                future.time = iterate_time
                                future_threading_groups.append(future)

                            if iterate_time == time1_end:
                                iterate_time = time2_start
                            elif iterate_time == time2_end:
                                iterate_time = time3_start
                            elif iterate_time == time3_end:
                                break
                            else:
                                iterate_time += datetime.timedelta(minutes=1)

                    FutureTreadingData.objects.bulk_create(future_threading_groups)

            else:
                with open(rootdir+"/"+filename, 'r') as f:
                    data_list = f.read().split('\n')
                    data_list = data_list[1:-3]
                    iterator = 0
                    first_row_data = data_list[iterator].split(',')
                    try:
                        first_row_time = datetime.datetime(*(time.strptime(first_row_data[0], "%Y/%m/%d %H:%M")[:6]))
                    except:
                        first_row_time = datetime.datetime(*(time.strptime(first_row_data[0], "%Y-%m-%d %H:%M")[:6]))
                    iterate_time = first_row_time

                    option_threading_groups = []

                    future_for_option = Future(code=filename.split('-')[0])
                    future_for_option.save()
                    option_for_treading_data = Option(code=filename.split('.')[0], asset=future_for_option)
                    option_for_treading_data.save()

                    while iterator < len(data_list):
                        try:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_list[iterator].split(' ')[0], "%Y/%m/%d"))[:6])
                        except:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_list[iterator].split(' ')[0], "%Y-%m-%d"))[:6])

                        time1_start = begin_date + datetime.timedelta(hours=8, minutes=55)
                        time1_end = begin_date + datetime.timedelta(hours=11, minutes=35)
                        time2_start = begin_date + datetime.timedelta(hours=13, minutes=25)
                        time2_end = begin_date + datetime.timedelta(hours=15, minutes=5)
                        time3_start = begin_date + datetime.timedelta(hours=20, minutes=55)
                        time3_end = begin_date + datetime.timedelta(hours=23, minutes=35)

                        if not (time1_start <= iterate_time <= time1_end or time2_start <= iterate_time <= time2_end or time3_start <= iterate_time <= time3_end):
                            iterator += 1

                        if iterator != 0:
                            iterate_time = time1_start

                        while (time1_start <= iterate_time <= time1_end) or (time2_start <= iterate_time <= time2_end) or (time3_start <= iterate_time <= time3_end):
                            # print(iterator)
                            if iterator == len(data_list):
                                break
                            # next_time = datetime.datetime.now()
                            try:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_list[iterator].split(',')[0],
                                                    "%Y/%m/%d %H:%M")[:6]))
                            except:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_list[iterator].split(',')[0],
                                                    "%Y-%m-%d %H:%M")[:6]))
                            if not ((time1_start <= next_time <= time1_end)
                                or (time2_start <= next_time <= time2_end)
                                or (time3_start <= next_time <= time3_end)):
                                iterator += 1
                                break
                            if iterate_time == next_time:
                                option = OptionTreadingData(time=iterate_time,
                                                            open_price=data_list[iterator].split(',')[1],
                                                            max_price=data_list[iterator].split(',')[2],
                                                            min_price=data_list[iterator].split(',')[3],
                                                            close_price=data_list[iterator].split(',')[4],
                                                            option=option_for_treading_data,
                                                            volume=float(data_list[iterator].split(',')[6]))
                                option_threading_groups.append(option)
                                iterator += 1
                            else:
                                option = copy.deepcopy(option_threading_groups[-1])
                                option.time = iterate_time
                                option_threading_groups.append(option)

                            if iterate_time == time1_end:
                                iterate_time = time2_start
                            elif iterate_time == time2_end:
                                iterate_time = time3_start
                            elif iterate_time == time3_end:
                                break
                            else:
                                iterate_time += datetime.timedelta(minutes=1)

                    OptionTreadingData.objects.bulk_create(option_threading_groups)


def physicals_data_transfer(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        data_list = f.read().split('\n')

        data_list = data_list[2:-3]
        datetime_format = '%Y-%m-%d'
        physicals_group = []
        for data in data_list:
            [p_time, price] = data.split(',')
            p_time = datetime.datetime.strptime(p_time, datetime_format)
            price = float(price)
            print(price)
            physical = Spot(time=p_time, price=price)
            physicals_group.append(physical)

        Spot.objects.bulk_create(physicals_group)

    print('finish')


def crop_data_transfer(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data_list = f.read().split('\n')

        data_list = data_list[2:-3]
        print(data_list)
        datetime_format = '%Y-%m-%d'
        physicals_group = []
        for data in data_list:
            [p_time, open_price, max_price, min_price, close_price, _, _, _, _] = data.split(',')
            p_time = datetime.datetime.strptime(p_time, datetime_format)
            open_price = float(open_price)
            max_price = float(max_price)
            min_price = float(min_price)
            close_price = float(close_price)
            physical = ContinuousDayFutureTreadingData(type='鸡蛋', time=p_time, open_price=open_price, max_price=max_price, min_price=min_price, close_price=close_price)
            physicals_group.append(physical)

        ContinuousDayFutureTreadingData.objects.bulk_create(physicals_group)

    print('finish')