from option.models import *
import itertools
import random
import time

def get_hedge_cost(future_list, option_list):

    return 5000

def monte_carlo(future_list, option_list, physicals, w1, w2, time_future, dist, time_now = None, max_cost = 50000, fmax = 50, omax = 50):
    if time_now == None:
        time_now_with_seconds = datetime.datetime.now()
        time_now = datetime.datetime(year=time_now_with_seconds.year, month=time_now_with_seconds.month, day=time_now_with_seconds.day
                                 , hour=time_now_with_seconds.hour, minute=time_now_with_seconds.minute)

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

    # if dist['type'] == 'normal':




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
    for i in range(1, 4):
        iter = itertools.combinations(fo_list_all, i)
        fo_list_combo.append(list(iter))


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
        hedge_cost = get_hedge_cost(combo['future_list'], combo['option_list'])
        if 0 < hedge_cost < max_cost:
            combo_chosen.append(combo)

    return combo_chosen




