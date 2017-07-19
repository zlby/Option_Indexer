from algorithm.interval.net_run import *
from option.models import *
import itertools


#
def initialize_interval():
    query_set = Option.objects.all()
    option_code_list = []
    for item in query_set:
        option_code_list.append(item.code)
    option_comb_list = list(itertools.combinations(option_code_list, 2))
    for comb in option_comb_list:
        Intervals.objects.create(positive_option_id=comb[0], negative_option_id=comb[1])
    print("finish")


def update_interval():
    # option_comb_list = initialize_interval()
    # for comb in option_comb_list:
    #     print(comb[0])
    #     print(comb[1])
    #     try:
    #         print(get_interval(comb[0], comb[1]))
    #     except:
    #         print("not enough data")

    query_set = Intervals.objects.all()
    for item in query_set:
        (lower_bound_a, upper_bound_a), (lower_bound_b, upper_bound_b), (lower_bound_c, upper_bound_c) = get_interval(
            item.positive_option_id, item.negative_option_id)
        item.lower_bound_a = lower_bound_a
        item.upper_bound_a = upper_bound_a
        item.lower_bound_b = lower_bound_b
        item.upper_bound_b = upper_bound_b
        item.lower_bound_c = lower_bound_c
        item.upper_bound_c = upper_bound_c

        item.save()