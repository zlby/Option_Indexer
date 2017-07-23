import itertools
from algorithm.interval.graph_build import *
from algorithm.data_provider.data_provider_django import *
from multiprocessing import Process, Lock


def initialize_interval():
    query_set = Option.objects.all()
    option_code_list = []
    for item in query_set:
        option_code_list.append(item.code)
    option_comb_list = list(itertools.combinations(option_code_list, 2))
    for comb in option_comb_list:
        Intervals.objects.create(positive_option_id=comb[0], negative_option_id=comb[1])
    print("finish")


def truncate_interval():
    Intervals.objects.all().delete()


def process_update(part_graph_builders):
    for part_graph_builder in part_graph_builders:
        spread_position = part_graph_builder.get__spread_position_of_combined_options()
        print(spread_position)
        if spread_position is not None:
            spread_position = -abs(spread_position)
            # TODO: check if the interval is correct
            (l_bound_a, u_bound_a), (l_bound_b, u_bound_b) = part_graph_builder.find_max_benefit_intervals(spread_position, 1)
            # TODO: use private attribute
            interval_obj = Intervals.objects.get(positive_option=part_graph_builder.positive_option_code,
                                                 negative_option=part_graph_builder.negative_option_code)
            interval_obj.lower_bound_a = l_bound_a
            interval_obj.upper_bound_a = u_bound_a
            interval_obj.lower_bound_b = l_bound_b
            interval_obj.upper_bound_b = u_bound_b
            interval_obj.rate = spread_position
            interval_obj.save()


def process_combination(lock, combinations, graph_builders, dp):
    process_graph_builders = []
    for combination in combinations:
        graph_builder = GraphBuilder(dp)
        graph_builder.prepare(combination.positive_option,
                              combination.negative_option,
                              2000)
        process_graph_builders.append(graph_builder)
    lock.acquire()
    try:
        graph_builders.extends(process_graph_builders)
    finally:
        lock.release()


def update_interval():
    truncate_interval()
    initialize_interval()
    combinations = Intervals.objects.all()
    graph_builders = []
    dp = DjangoDataProvider()

    lock = Lock()
    core_num = 8
    process_len = int(len(combinations) / core_num)
    remain_len = len(combinations) % core_num

    mark = 0
    for i in range(8):
        if i < remain_len:
            extra = 1
        else:
            extra = 0
        p = Process(target=process_combination, args=(lock,
                                                      combinations[mark:mark+process_len+extra],
                                                      graph_builders,
                                                      dp))
        print(i)
        p.start()

    process_update(graph_builders)

# 子进程要执行的代码
# def run_proc(name):
#     for j in range(100000):
#         print(name)
#
# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     for i in range(8):
#         p = Process(target=run_proc, args=(i,))
#         print('Process will start.')
#         p.start()
#     print('Process end.')