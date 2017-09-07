from option.models import *
import itertools
import random
import time
from algorithm.prediction.data_analyzer.regress_model import *
import numpy as np
from gain_loss.option_price_cal import get_option_price



def monte_carlo(future_list, option_list, physicals, w1, w2, time_future, dist, time_now = None, max_cost = 50000, fmax = 50, omax = 50):
    if time_now == None:
        time_now_with_seconds = datetime.datetime.now()
        time_now = datetime.datetime(year=time_now_with_seconds.year, month=time_now_with_seconds.month, day=time_now_with_seconds.day
                                 , hour=time_now_with_seconds.hour, minute=time_now_with_seconds.minute)
        # time_now = datetime.datetime(2017, 7, 12, 11, 32)
    time_today = datetime.datetime(year=time_now.year, month=time_now.month, day=time_now.day)
    time_delt = time_future - time_today
    t = time_delt.days / 365
    time_future_with_min = time_now + time_delt

    for i in range(len(future_list)):
        future_list[i]['current_price'] = FutureTreadingData.objects.get(time=time_now, future=future_list[i]['code'])
    for i in range(len(option_list)):
        option_list[i]['current_price'] = OptionTreadingData.objects.get(time=time_now, option=option_list[i]['code'])

    total_future_tv0 = 0
    total_option_tv0 = 0

    for i in range(len(future_list)):
        total_future_tv0 += future_list[i]['price'] * future_list[i]['amount']
    for i in range(len(option_list)):
        total_option_tv0 += option_list[i]['price'] * option_list[i]['amount']

    spot_price_now = Spot.objects.get(time=time_now)

    total_asset_tv0 = 10 * (spot_price_now * physicals) + 10 * total_future_tv0 + 10 * total_option_tv0

    combo_list = choose_combos(max_cost, fmax, omax)

    futures_in_list = []
    options_in_list = []

    query = Future.objects.all()
    for qu in query:
        dic = {}
        dic['code'] = qu.code
        futures_in_list.append(dic)

    for combo_dict in combo_list:
        # for future in combo_dict['future_list']:
        #     flag = False
        #     for item in futures_in_list:
        #         if future['code'] == item['code']:
        #             flag = True
        #             break
        #     if not flag:
        #         futures_in_list.append(future)
        for option in combo_dict['option_list']:
            flag = False
            for item in options_in_list:
                if option['code'] == item['code']:
                    flag = True
                    break
            if not flag:
                options_in_list.append(option)

    for i in range(len(futures_in_list)):
        future_data_list = []
        query_set_future = HourFutureTreadingData.objects.filter(future=futures_in_list[i]['code']).order_by('-time')[:20]
        future_time_start = query_set_future[len(query_set_future) - 1].time
        for j in range(len(query_set_future)):
            future_data_list.insert(0, query_set_future[i].close_price)

        spot_time_start = future_time_start - time_delt
        spot_data_list = []
        query_set_spot = Spot.objects.filter(time__gte=spot_time_start).order_by('time')[:20]
        if len(query_set_spot) < 20:
            query_set_spot = Spot.objects.all().order_by('-time')[:20]
            for j in range(len(query_set_spot)):
                spot_data_list.insert(0, query_set_spot[j].price)
        else:
            for j in range(len(query_set_spot)):
                spot_data_list.append(query_set_spot[j].price)


        u, y = regress(spot_data_list, future_data_list, t)
        futures_in_list[i]['u'] = u
        futures_in_list[i]['y'] = y


    spot_price_list = []

    if dist['type'] == 'normal':
        for _ in range(100):
            spot_price_list.append(np.random.normal(dist['argv'][0], dist['argv'][1]))
    if dist['type'] == 'triangle':
        for _ in range(100):
            spot_price_list.append(np.random.triangular(dist['argv'][0], dist['argv'][1], dist['argv'][2]))
    if dist['type'] == 'uniform':
        for _ in range(100):
            spot_price_list.append(np.random.uniform(dist['argv'][0], dist['argv'][1]))

    if len(spot_price_list) != 100:
        return None

    for spot_price in spot_price_list:
        for future in futures_in_list:
            future['price'] = (spot_price + future['u']) * np.exp((np.log(1.03) - future['y']) * t)

        for i in range(len(options_in_list)):
            option_code = options_in_list[i]['code']
            future_code = option_code.split('-')[0]
            for future in futures_in_list:
                if future['code'] == future_code:
                    options_in_list[i]['future_price'] = future['price']
                    break
            if options_in_list[i]['volatility'] is None:
                option_price = get_option_price(options_in_list[i]['code'], time_future_with_min, 2000, price=options_in_list[i]['future_price'])
            else:
                option_price = get_option_price(options_in_list[i]['code'], time_future_with_min, 2000, price=options_in_list[i]['future_price'],
                                                volat=options_in_list[i]['volatility'])
            options_in_list[i]['price'] = option_price




def choose_combos(max_cost=50000, fmax=50, omax=50):

    time1 = time.clock()
    query_set_future = Future.objects.all()
    query_set_option = Option.objects.all()
    fo_list_all = []
    fo_list_combo = []

    combo_all = []
    combo_chosen = []

    for future in query_set_future:
        fo_list_all.append(future.code)
    for option in query_set_option:
        fo_list_all.append(option.code)
    for i in range(1, 3):
        iter = itertools.combinations(fo_list_all, i)
        fo_list_combo.append(list(iter))
    print(fo_list_combo)


    for combo_list in fo_list_combo:
        for combo in combo_list:
            dict_combo = {}
            dict_combo['future_list'] = []
            dict_combo['option_list'] = []
            for code in combo:
                dict_code = {}
                dict_code['code'] = code
                if code.find('-') == -1:
                    dict_combo['future_list'].append(dict_code)
                else:
                    dict_combo['option_list'].append(dict_code)
            for _ in range(10):
                new_combo = {}
                new_combo['future_list'] = []
                new_combo['option_list'] = []
                for future_dict in dict_combo['future_list']:
                    fu = {}
                    fu['code'] = future_dict['code']
                    fu['amount'] = random.randint(1, fmax)
                    new_combo['future_list'].append(fu)
                for option_dict in dict_combo['option_list']:
                    op = {}
                    op['code'] = option_dict['code']
                    op['amount'] = random.randint(1, omax)
                    new_combo['option_list'].append(op)
                combo_all.append(new_combo)


    for combo in combo_all:
        hedge_cost = 1
        if 0 < hedge_cost < max_cost:
            combo_chosen.append(combo)

    return combo_chosen



