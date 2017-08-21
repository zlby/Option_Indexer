from gain_loss.regress_model import *
from gain_loss.option_price_cal import *
from option.models import *
import datetime

def get_ass(future_code_list, future_quantity_list, option_code_list, option_quantity_list, spot_price, spot_quantity, t_delta: datetime.timedelta, option_vol_list = None):
    if (len(future_code_list) != len(future_quantity_list)) or (len(option_code_list) != len(option_quantity_list) or (len(option_code_list) != len(option_vol_list))):
        return None

    future_price_list = []

    for future_code in future_code_list:
        future_data_list = []
        query_set = FutureTreadingData.objects.filter(future=future_code).order_by('-time')[:1000]
        future_time_start = query_set[len(query_set) - 1].time
        for i in range(len(query_set)):
            future_data_list.insert(0, query_set[i].close_price)

        spot_time_start = future_time_start - t_delta
        spot_data_list = []
        query_set_spot = Spot.objects.filter(time__gte=spot_time_start).order_by('time')[:1000]
        for i in range(len(query_set_spot)):
            spot_data_list.append(query_set_spot[i].price)

        if (len(future_data_list) != len(spot_data_list)):
            return None

        t = t_delta.days / 365
        u, y = regress(spot_data_list, future_data_list, t)
        future_price = (spot_price + u) * np.exp((np.log(1.03) - y) * t)
        future_price_list.append(future_price)

    future_dict = {}
    for i in range(future_code_list):
        future_dict[future_code_list[i]] = future_price_list[i]


    option_dict = {}
    for i in len(option_code_list):
        option_code = option_code_list[i]
        future_code = option_code.split('-')[0]
        future_price = future_dict[future_code]

        time_now = datetime.datetime.now()
        time_future = time_now + t_delta

        if option_vol_list == None:
            option_price = get_option_price(option_code, time_future, 2000, price=future_price)
        else:
            option_price = get_option_price(option_code, time_future, 2000, price=future_price, volat=option_vol_list[i])
        option_dict[option_code] = [option_price]

    total_future = 0
    total_option = 0
    for i in range(len(future_code_list)):
        total_future += future_quantity_list[i] * future_price_list[i]

    for i in range(len(option_code_list)):
        total_option += option_quantity_list[i] * option_dict[option_code_list[i]]

    total_asset = 10 * (spot_price * spot_quantity) + 10 * total_future + 10 * total_option

    return total_asset