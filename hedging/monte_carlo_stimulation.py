from option.models import *

def monte_carlo(future_list, option_list, physicals, w1, w2, time_future, time_now = None, max_cost = 50000, fmax = 50, omax = 50):
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


