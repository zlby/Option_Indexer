from option.models import *
import itertools

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
    pass