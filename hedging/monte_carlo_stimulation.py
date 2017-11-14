from option.models import *
import itertools
import random
import datetime
import time
from algorithm.prediction.data_analyzer.regress_model import *
import numpy as np
from gain_loss.option_price_cal import get_option_price
import algorithm.prediction.data_analyzer.calculate_hedge_cost as chc
from gain_loss.history_vol import history_vol
from hedging.spot_price_distribution import get_predict


def monte_carlo(future_list, option_list, physicals:float, w1:float, w2:float, time_future:datetime.datetime, dist, max_cost = 50000., fmax:int = 50, omax:int = 50, time_now = None):
    # time_bg = time.clock()
    if time_now is None:
        time_now_with_seconds = datetime.datetime.now()
        time_now = datetime.datetime(year=time_now_with_seconds.year, month=time_now_with_seconds.month, day=time_now_with_seconds.day
                                 , hour=time_now_with_seconds.hour, minute=time_now_with_seconds.minute)
        # time_now = datetime.datetime(2017, 7, 12, 11, 32)
    time_today = datetime.datetime(year=time_now.year, month=time_now.month, day=time_now.day)
    time_delt = time_future - time_today
    t = time_delt.days / 365
    time_future_with_min = time_now + time_delt

    for i in range(len(future_list)):
        try:
            future_list[i]['current_price'] = FutureTreadingData.objects.get(time=time_now, future=future_list[i]['code']).close_price
        except:
            future_list[i]['current_price'] = FutureTreadingData.objects.filter(future=future_list[i]['code']).order_by('-time')[0].close_price
    for i in range(len(option_list)):
        try:
            option_list[i]['current_price'] = OptionTreadingData.objects.get(time=time_now, option=option_list[i]['code']).close_price
        except:
            option_list[i]['current_price'] = OptionTreadingData.objects.filter(option=option_list[i]['code']).order_by('-time')[0].close_price

    total_future_tv0 = 0
    total_option_tv0 = 0

    for i in range(len(future_list)):
        total_future_tv0 += future_list[i]['current_price'] * future_list[i]['amount']
    for i in range(len(option_list)):
        total_option_tv0 += option_list[i]['current_price'] * option_list[i]['amount']

    spot_price_now = 0
    try:
        spot_price_now = Spot.objects.get(time=time_now).price
    except:
        spot_price_now = Spot.objects.all().order_by('-time')[0].price

    total_asset_tv0 = (float(spot_price_now) * float(physicals)) + 10 * float(total_future_tv0) + 10 * float(total_option_tv0)


    combo_list = choose_combos(time_future, max_cost, fmax, omax)

    for combo in combo_list:
        combo['v_list'] = []
        combo['v0_minus_v_list'] = []

        combo['future_together'] = []
        combo['option_together'] = []

        for future in combo['future_list']:
            combo['future_together'].append(future)
        for option in combo['option_list']:
            combo['option_together'].append(option)


        for future in future_list:
            combo['future_together'].append(future)
        for option in option_list:
            combo['option_together'].append(option)


    futures_in_list = []
    options_in_list = []

    query = Future.objects.all()
    for qu in query:
        dic = {}
        dic['code'] = qu.code
        futures_in_list.append(dic)

    for combo_dict in combo_list:

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
        query_set_future = FutureTreadingData.objects.filter(future=futures_in_list[i]['code']).order_by('-time')[:20]
        if len(query_set_future) != 20:
            return None
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
        for _ in range(20):
            spot_price_list.append(np.random.normal(float(dist['argv'][0]), float(dist['argv'][1])))
    if dist['type'] == 'triangle':
        for _ in range(20):
            spot_price_list.append(np.random.triangular(float(dist['argv'][0]), float(dist['argv'][1]), float(dist['argv'][2])))
    if dist['type'] == 'uniform':
        for _ in range(20):
            spot_price_list.append(np.random.uniform(float(dist['argv'][0]), float(dist['argv'][1])))
    if dist['type'] == 'predict':
        for _ in range(20):
            spot_price_list.append(np.random.normal(get_predict(time_future), 1))

    if len(spot_price_list) != 20:
        return None

    for spot_price in spot_price_list:
        for future in futures_in_list:
            future['price'] = abs((spot_price + future['u']) * np.exp((np.log(1.03) - future['y']) * t))

        for i in range(len(options_in_list)):
            option_code = options_in_list[i]['code']
            future_code = option_code.split('-')[0]
            for future in futures_in_list:
                if future['code'] == future_code:
                    options_in_list[i]['future_price'] = future['price']
                    break
            # code is wrong here
            # if options_in_list[i]['volatility'] is None:
            #     option_price = get_option_price(options_in_list[i]['code'], time_future_with_min, 2000, price=options_in_list[i]['future_price'])
            # else:
            #     option_price = get_option_price(options_in_list[i]['code'], time_future_with_min, 2000, price=options_in_list[i]['future_price'],
            #                                     volat=options_in_list[i]['volatility'])
            # options_in_list[i]['price'] = option_price

            # new code
            strike_price = option_code[8:]
            strike_price = float(strike_price)
            options_in_list[i]['price'] = max(options_in_list[i]['future_price'] - strike_price, 0)

        # 计算vi
        for combo in combo_list:
            total_future_tv = 0
            total_option_tv = 0



            for future in combo['future_together']:
                for item in futures_in_list:
                    if future['code'] == item['code']:
                        # future['price'] = item['price']
                        total_future_tv += item['price'] * future['amount']
                        break
            for option in combo['option_together']:
                for item in options_in_list:
                    if option['code'] == item['code']:
                        # option['price'] = item['price']
                        total_option_tv += item['price'] * option['amount']

            total_asset_tv = (float(spot_price_now) * float(physicals)) + 10 * float(total_future_tv) + 10 * float(total_option_tv) - combo['hedge_cost']
            combo['v_list'].append(total_asset_tv)
            combo['v0_minus_v_list'].append(total_asset_tv0 - total_asset_tv)

    P1_list = []
    P2_list = []
    for combo in combo_list:
        combo['P2_add_value'] = 0
        for value in combo['v0_minus_v_list']:
            combo['P2_add_value'] += value
        combo['P2_value'] = abs(combo['P2_add_value'])
        P1_list.append(combo['hedge_cost'])
        P2_list.append(combo['P2_value'])

    P1_list.sort(reverse=True)
    P2_list.sort(reverse=True)
    for combo in combo_list:
        for i1 in range(len(P1_list)):
            if P1_list[i1] == combo['hedge_cost']:
                combo['P1'] = (i1 + 1) / len(P1_list)
                break
        for i2 in range(len(P2_list)):
            if P2_list[i2] == combo['P2_value']:
                combo['P2'] = (i2 + 1) / len(P2_list)
                break

        combo['score'] = float(combo['P1']) * float(w1) + float(combo['P2']) * float(w2)

    # combo_list.sort(key=lambda co : co['score'], reverse=True)
    # result_combo = combo_list[0]


    # for item in combo_list:
    #     print(item['score'], item['future_list'], item['option_list'], item['P1'], item['P2'])


    result_combo = {}
    result_combo['score'] = combo_list[0]['score']

    for combo in combo_list:
        if combo['score'] > result_combo['score']:
            result_combo['hedge_cost'] = combo['hedge_cost']
            result_combo['future_list'] = []
            result_combo['option_list'] = []
            for fute in combo['future_list']:
                fut = {}
                fut['code'] = fute['code']
                fut['amount'] = fute['amount']
                result_combo['future_list'].append(fut)
            for opti in combo['option_list']:
                opt = {}
                opt['code'] = opti['code']
                opt['amount'] = opti['amount']
                result_combo['option_list'].append(opt)

    # time_com = time.clock()



    return result_combo['future_list'], result_combo['option_list']




def choose_combos(time_future:datetime.datetime, max_cost:float=50000, fmax=50, omax=50):

    query_set_future = Future.objects.filter(delivery_day__gt = time_future)

    fo_list_all = []
    fo_list_combo = []

    combo_all = []
    combo_chosen = []

    for future in query_set_future:
        fo_list_all.append(future.code)

    query_set_option = Option.objects.filter(asset__in=fo_list_all)

    for option in query_set_option:
        fo_list_all.append(option.code)

    for i in range(1, 3):
        iter = itertools.combinations(fo_list_all, i)
        fo_list_combo.append(list(iter))

    option_code_price_deposit_list = []
    future_code_price_deposit_list = []
    query_o = Option.objects.all()
    query_f = Future.objects.all()
    for item in query_o:
        dict_ocp = {}
        dict_ocp['code'] = item.code
        dict_ocp['current_price'] = OptionTreadingData.objects.filter(option=dict_ocp['code']).order_by('-time')[0].close_price
        dict_ocp['deposit_today'] = Option.objects.get(code=dict_ocp['code']).deposit_today
        try:
            dict_ocp['volatility'] = history_vol(dict_ocp['code'])
        except:
            dict_ocp['volatility'] = 0.1
        option_code_price_deposit_list.append(dict_ocp)

    for item in query_f:
        dict_fcp = {'code': item.code}
        dict_fcp['current_price'] = FutureTreadingData.objects.filter(future=dict_fcp['code']).order_by('-time')[0].close_price
        dict_fcp['deposit_today'] = Future.objects.get(code=dict_fcp['code']).deposit_today
        future_code_price_deposit_list.append(dict_fcp)

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
                    fu['amount'] = random.randint(-fmax, fmax)
                    if fu['amount'] == 0:
                        fu['amount'] = random.randint(1, fmax)
                    for item in future_code_price_deposit_list:
                        if fu['code'] == item['code']:
                            fu['price'] = item['current_price']
                            fu['deposit'] = item['deposit_today']
                            break
                    new_combo['future_list'].append(fu)
                for option_dict in dict_combo['option_list']:
                    op = {}
                    op['code'] = option_dict['code']
                    op['amount'] = random.randint(-omax, omax)
                    if op['amount'] == 0:
                        op['amount'] = random.randint(1, omax)
                    for item in option_code_price_deposit_list:
                        if op['code'] == item['code']:
                            op['price'] = item['current_price']
                            op['deposit'] = item['deposit_today']
                            op['volatility'] = item['volatility']
                            break
                    new_combo['option_list'].append(op)
                combo_all.append(new_combo)


    for combo in combo_all:
        dict_none = {'amount': 0, 'code': None, 'deposit': 0, 'price': 0}
        option_list = combo['option_list']
        future_list = combo['future_list']
        c_l = []
        c_s = []
        p_l = []
        p_s = []
        f_l = []
        f_s = []

        for option in option_list:
            if option['code'].find('p') == -1:
                if option['amount'] >= 0:
                    c_l.append(option)
                else:
                    new_op = option
                    new_op['amount'] = abs(option['amount'])
                    c_s.append(new_op)
            else:
                if option['amount'] >= 0:
                    p_l.append(option)
                else:
                    new_op = option
                    new_op['amount'] = abs(option['amount'])
                    c_s.append(new_op)
        for future in future_list:
            if future['amount'] >= 0:
                f_l.append(future)
            else:
                new_fu = future
                new_fu['amount'] = abs(future['amount'])
                f_s.append(new_fu)


        if len(c_l) == 0:
            c_l.append(dict_none)
        if len(c_s) == 0:
            c_s.append(dict_none)
        if len(p_l) == 0:
            p_l.append(dict_none)
        if len(p_s) == 0:
            p_s.append(dict_none)
        if len(f_l) == 0:
            f_l.append(dict_none)
        if len(f_s) == 0:
            f_s.append(dict_none)

        combo['hedge_cost'] = chc.hedge_cost(c_l, c_s, p_l, p_s, f_l, f_s)
        if 0. < combo['hedge_cost'] < max_cost:
            combo_chosen.append(combo)


    return combo_chosen



