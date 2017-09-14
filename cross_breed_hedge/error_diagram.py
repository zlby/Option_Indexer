from cross_breed_hedge.transaction_rate import *

def show_diagram(spot_list, future_list, time_list):
    if len(spot_list) != len(future_list) or len(spot_list) != len(time_list):
        return None

    diff_spot = get_diff(spot_list)
    diff_future = get_diff(future_list)

    rate = OLS(diffx=diff_future, diffy=diff_spot)

    x_list = []
    y_list = []

    for i in range(1, len(time_list)):
        x_list.append(time_list[i])

    for i in range(len(diff_spot)):
        y_list.append(diff_spot[i]/ spot_list[i+1] - rate * (diff_future[i]/future_list[i+1]))

    result_list = []
    for x, y in zip(x_list, y_list):
        result_list.append((x, y))

    return result_list