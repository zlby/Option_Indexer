from algorithm.prediction.data_analyzer.regress_model import *
from gain_loss.option_price_cal import *
from option.models import *
import datetime
# import matplotlib.pyplot as plt

# def get_asss(future_code_list, future_quantity_list, option_code_list, option_quantity_list, spot_price, spot_quantity, t_delta: datetime.timedelta, option_vol_list = None):
#     if (len(future_code_list) != len(future_quantity_list)) or (len(option_code_list) != len(option_quantity_list) or (len(option_code_list) != len(option_vol_list))):
#         return None
#
#     future_price_list = []
#
#     for future_code in future_code_list:
#         future_data_list = []
#         query_set = FutureTreadingData.objects.filter(future=future_code).order_by('-time')[:1000]
#         future_time_start = query_set[len(query_set) - 1].time
#         for i in range(len(query_set)):
#             future_data_list.insert(0, query_set[i].close_price)
#
#         spot_time_start = future_time_start - t_delta
#         spot_data_list = []
#         query_set_spot = Spot.objects.filter(time__gte=spot_time_start).order_by('time')[:1000]
#         for i in range(len(query_set_spot)):
#             spot_data_list.append(query_set_spot[i].price)
#
#         if (len(future_data_list) != len(spot_data_list)):
#             return None
#
#         t = t_delta.days / 365
#         u, y = regress(spot_data_list, future_data_list, t)
#         future_price = (spot_price + u) * np.exp((np.log(1.03) - y) * t)
#         future_price_list.append(future_price)
#
#     future_dict = {}
#     for i in range(future_code_list):
#         future_dict[future_code_list[i]] = future_price_list[i]
#
#
#     option_dict = {}
#     for i in len(option_code_list):
#         option_code = option_code_list[i]
#         future_code = option_code.split('-')[0]
#         future_price = future_dict[future_code]
#
#         time_now = datetime.datetime.now()
#         time_future = time_now + t_delta
#
#         if option_vol_list == None:
#             option_price = get_option_price(option_code, time_future, 2000, price=future_price)
#         else:
#             option_price = get_option_price(option_code, time_future, 2000, price=future_price, volat=option_vol_list[i])
#         option_dict[option_code] = [option_price]
#
#     total_future = 0
#     total_option = 0
#     for i in range(len(future_code_list)):
#         total_future += future_quantity_list[i] * future_price_list[i]
#
#     for i in range(len(option_code_list)):
#         total_option += option_quantity_list[i] * option_dict[option_code_list[i]]
#
#     total_asset = 10 * (spot_price * spot_quantity) + 10 * total_future + 10 * total_option
#
#     return total_asset


def get_ass(time_future: datetime.datetime, physicals: float, future_list, option_list, time_now = None):

    physicals = float(physicals)
    # 若time_now取默认值None，则计算当前时间，若传入历史时间，则计算历史时间
    if time_now == None:
        time_now_with_seconds = datetime.datetime.now()
        time_now = datetime.datetime(year=time_now_with_seconds.year, month=time_now_with_seconds.month, day=time_now_with_seconds.day
                                 , hour=time_now_with_seconds.hour, minute=time_now_with_seconds.minute)
        # time_now = datetime.datetime(2017, 7, 12, 11, 32)
    time_today = datetime.datetime(year=time_now.year, month=time_now.month, day=time_now.day)
    time_delt = time_future - time_today
    t = time_delt.days / 365
    time_future_with_min = time_now + time_delt
    try:
        spot_price_now = Spot.objects.get(time=time_now).price
    except:
        spot_price_now = Spot.objects.all().order_by('-time')[0].price

    for i in range(len(future_list)):
        future_data_list = []
        query_set_future = FutureTreadingData.objects.filter(future=future_list[i]['code']).order_by('-time')[:20]
        if len(query_set_future) != 20:
            future_list[i]['u'] = 1
            future_list[i]['y'] = 1
            continue
        else:
            future_time_start = query_set_future[len(query_set_future) - 1].time
        for j in range(len(query_set_future)):
            future_data_list.insert(0, query_set_future[j].close_price)

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
        future_list[i]['u'] = u
        future_list[i]['y'] = y
        

    spot_price_low = 0.5 * spot_price_now
    spot_price_high = 1.5 * spot_price_now
    step_forward = (spot_price_high - spot_price_low) / 99
    total_asset_coordinate_list = []
    # x_list=[]
    # y_list=[]

    future_list_all = []

    query_set_future_all = Future.objects.all()
    for future in query_set_future_all:
        dict = {}
        dict['code'] = future.code
        future_list_all.append(dict)

    for i in range(len(future_list_all)):
        future_data_list = []
        query_set_future = FutureTreadingData.objects.filter(future=future_list_all[i]['code']).order_by('-time')[:20]
        if len(query_set_future) != 20:
            future_list_all[i]['u'] = 1
            future_list_all[i]['y'] = 1
            continue
        else:
            future_time_start = query_set_future[len(query_set_future) - 1].time
        for j in range(len(query_set_future)):
            future_data_list.insert(0, query_set_future[j].close_price)

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
        future_list_all[i]['u'] = u
        future_list_all[i]['y'] = y



    for j in range(100):
        total_future = 0
        total_option = 0
        stimulate_price = spot_price_low + j * step_forward

        for i in range(len(future_list)):
            future_list[i]['price'] = (stimulate_price + future_list[i]['u']) * np.exp((np.log(1.03) - future_list[i]['y']) * t)
            total_future += future_list[i]['price'] * future_list[i]['amount']
        for i in range(len(future_list_all)):
            future_list_all[i]['price'] = (stimulate_price + future_list_all[i]['u']) * np.exp((np.log(1.03) - future_list_all[i]['y']) * t)
        for i in range(len(option_list)):
            option_code = option_list[i]['code']
            future_code = option_code.split('-')[0]
            for future in future_list_all:
                if future['code'] == future_code:
                    option_list[i]['future_price'] = future['price']
                    break
            if option_list[i]['volatility'] is None:
                option_price = get_option_price(option_list[i]['code'], time_future_with_min, 2000, price=option_list[i]['future_price'])
            else:
                option_price = get_option_price(option_list[i]['code'], time_future_with_min, 2000, price=option_list[i]['future_price'],
                                                volat=option_list[i]['volatility'])
            option_list[i]['price'] = option_price
            total_option += option_list[i]['price'] * option_list[i]['amount']


        total_asset = (stimulate_price * physicals) + 10 * total_future + 10 * total_option
        total_asset_coordinate_list.append((stimulate_price, total_asset))

        # x_list.append(stimulate_price)
        # y_list.append(total_asset)

    # plt.plot(x_list, y_list)
    # plt.show()

    return total_asset_coordinate_list
