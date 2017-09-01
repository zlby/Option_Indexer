import datetime
import time
import copy
import os
from option.models import FutureTreadingData, OptionTreadingData, Future, Option
import warnings

warnings.filterwarnings("ignore")


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

            with open(rootdir + "/" + filename, 'r') as f:
                data_list = f.read().split('\n')
                data_list = data_list[1:-3]

                try:
                    data_time_list = [datetime.datetime(
                        *(time.strptime(data.split(' ')[0], "%Y/%m/%d"))[:6]) for data in data_list]
                except:
                    data_time_list = [datetime.datetime(
                        *(time.strptime(data.split(' ')[0], "%Y-%m-%d"))[:6]) for data in data_list]

                # data_time_reduce_list = []
                # for data_time in data_time_list:
                #     if data_time not in data_time_reduce_list:
                #         data_time_reduce_list += [data_time]
                #
                # print(data_time_reduce_list)

                data_filted_list = []
                iter_mark = 0

                iter_date = data_time_list[0]
                while iter_date != data_time_list[-1] + datetime.timedelta(days=1):
                    if iter_date == data_time_list[iter_mark]:
                        if 0 <= iter_date.weekday() < 5:
                            data_filted_list.append(data_list[iter_mark])
                        iter_mark += 1
                        if iter_mark == len(data_time_list) or data_time_list[iter_mark-1] != data_time_list[iter_mark]:
                            iter_date += datetime.timedelta(days=1)
                        continue
                    else:
                        if 0 <= iter_date.weekday() < 5:
                            data_filted_list.append(
                                iter_date.strftime("%Y/%m/%d ") + data_list[iter_mark - 1].split(' ')[1])
                    iter_date += datetime.timedelta(days=1)


            print(filename)

            if "-" not in filename:
                    iterator = 0

                    first_row_data = data_filted_list[iterator].split(',')
                    try:
                        first_row_time = datetime.datetime(*(time.strptime(first_row_data[0], "%Y/%m/%d %H:%M")[:6]))
                    except:
                        first_row_time = datetime.datetime(*(time.strptime(first_row_data[0], "%Y-%m-%d %H:%M")[:6]))
                    iterate_time = first_row_time

                    future_threading_groups = []

                    future_for_treading_data = Future.objects.get(code=filename.split('.')[0])
                    # future_for_treading_data.save()

                    while iterator != len(data_filted_list):
                        try:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_filted_list[iterator].split(' ')[0], "%Y/%m/%d"))[:6])
                        except:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_filted_list[iterator].split(' ')[0], "%Y-%m-%d"))[:6])

                        time1_start = begin_date + datetime.timedelta(hours=8, minutes=55)
                        time1_end = begin_date + datetime.timedelta(hours=11, minutes=35)
                        time2_start = begin_date + datetime.timedelta(hours=13, minutes=25)
                        time2_end = begin_date + datetime.timedelta(hours=15, minutes=5)
                        time3_start = begin_date + datetime.timedelta(hours=20, minutes=55)
                        time3_end = begin_date + datetime.timedelta(hours=23, minutes=35)

                        # if not (time1_start <= iterate_time <= time1_end or time2_start <= iterate_time <= time2_end or time3_start <= iterate_time <= time3_end):
                        #     iterator += 1

                        if iterator != 0:
                            iterate_time = time1_start

                        while time1_start <= iterate_time <= time1_end or time2_start <= iterate_time <= time2_end or time3_start <= iterate_time <= time3_end:
                            while iterator == len(data_filted_list):
                                if iterate_time == time1_end:
                                    iterate_time = time2_start
                                elif iterate_time == time2_end:
                                    iterate_time = time3_start
                                elif iterate_time == time3_end:
                                    break
                                iterate_time += datetime.timedelta(minutes=1)
                            if iterate_time == time3_end and iterator == len(data_filted_list):
                                break
                            try:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_filted_list[iterator].split(',')[0],
                                                    "%Y/%m/%d %H:%M")[:6]))
                            except:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_filted_list[iterator].split(',')[0],
                                                    "%Y-%m-%d %H:%M")[:6]))
                            # if not ((time1_start <= next_time <= time1_end)
                            #     or (time2_start <= next_time <= time2_end)
                            #     or (time3_start <= next_time <= time3_end)):
                            #     iterator += 1
                            #     break
                            if iterate_time == next_time:
                                future = FutureTreadingData(time=iterate_time,
                                                            open_price=data_filted_list[iterator].split(',')[1],
                                                            max_price=data_filted_list[iterator].split(',')[2],
                                                            min_price=data_filted_list[iterator].split(',')[3],
                                                            close_price=data_filted_list[iterator].split(',')[4],
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
                            elif iterate_time <= next_time:
                                iterate_time += datetime.timedelta(minutes=1)
                            elif iterate_time > next_time:
                                iterator += 1

                    mid = (int)(len(future_threading_groups)/2)
                    FutureTreadingData.objects.bulk_create(future_threading_groups[:mid])
                    FutureTreadingData.objects.bulk_create(future_threading_groups[mid:])

            else:
                    iterator = 0
                    first_row_data = data_filted_list[iterator].split(',')
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

                    while iterator < len(data_filted_list):
                        try:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_filted_list[iterator].split(' ')[0], "%Y/%m/%d"))[:6])
                        except:
                            begin_date = datetime.datetime(
                                *(time.strptime(data_filted_list[iterator].split(' ')[0], "%Y-%m-%d"))[:6])

                        time1_start = begin_date + datetime.timedelta(hours=8, minutes=55)
                        time1_end = begin_date + datetime.timedelta(hours=11, minutes=35)
                        time2_start = begin_date + datetime.timedelta(hours=13, minutes=25)
                        time2_end = begin_date + datetime.timedelta(hours=15, minutes=5)
                        time3_start = begin_date + datetime.timedelta(hours=20, minutes=55)
                        time3_end = begin_date + datetime.timedelta(hours=23, minutes=35)

                        # if not (time1_start <= iterate_time <= time1_end or time2_start <= iterate_time <= time2_end or time3_start <= iterate_time <= time3_end):
                        #     iterator += 1

                        if iterator != 0:
                            iterate_time = time1_start

                        while (time1_start <= iterate_time <= time1_end) or (time2_start <= iterate_time <= time2_end) or (time3_start <= iterate_time <= time3_end):
                            while iterator == len(data_filted_list):
                                if iterate_time == time1_end:
                                    iterate_time = time2_start
                                elif iterate_time == time2_end:
                                    iterate_time = time3_start
                                elif iterate_time == time3_end:
                                    break
                                iterate_time += datetime.timedelta(minutes=1)
                            if iterate_time == time3_end and iterator == len(data_filted_list):
                                break
                            # next_time = datetime.datetime.now()
                            try:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_filted_list[iterator].split(',')[0],
                                                    "%Y/%m/%d %H:%M")[:6]))
                            except:
                                next_time = datetime.datetime(
                                    *(time.strptime(data_filted_list[iterator].split(',')[0],
                                                    "%Y-%m-%d %H:%M")[:6]))
                            # if not ((time1_start <= next_time <= time1_end)
                            #     or (time2_start <= next_time <= time2_end)
                            #     or (time3_start <= next_time <= time3_end)):
                            #     iterator += 1
                            #     break
                            if iterate_time == next_time:
                                option = OptionTreadingData(time=iterate_time,
                                                            open_price=data_filted_list[iterator].split(',')[1],
                                                            max_price=data_filted_list[iterator].split(',')[2],
                                                            min_price=data_filted_list[iterator].split(',')[3],
                                                            close_price=data_filted_list[iterator].split(',')[4],
                                                            option=option_for_treading_data,
                                                            volume=float(data_filted_list[iterator].split(',')[6]))
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
                            elif iterate_time <= next_time:
                                iterate_time += datetime.timedelta(minutes=1)
                            elif iterate_time > next_time:
                                iterator += 1

                    OptionTreadingData.objects.bulk_create(option_threading_groups)
    # print("complete!")
