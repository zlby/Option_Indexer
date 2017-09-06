"""此模块全部作废"""

from option.models import *

# HEDGE COST=
# Σ （各看涨期权空头持有手数*对应看涨期权空头保证金）
# +Σ（各看跌期权空头持有手数*对应看跌期权保证金）
# + （看涨期权空头总手数+看涨期权多头总手数+看跌期权空头总手数+看跌期权多头总手数）*1
# -Σ （看涨期权空头手数*数据库中对应看涨期权的最近价格 +看跌期权空头手数*数据库中对应看跌期权的最近价格）*10
# +Σ  (看涨期权多头手数*数据库中对应看涨期权最近价格+看跌期权多头手数*数据库中对应看跌期权最近价格）*10
# +Σ（豆粕期货空头持有手数*对应的豆粕期货保证金）
# +Σ（豆粕期权多头持有手数*对应的豆粕期货保证金）
# + （豆粕期货空头手数+豆粕期货多头手数）*1.5

def _split_option_list(option_list):

    a = [(x['code'], x['amount'], Option.objects.get(code=x['code']).deposit_today)
         for x in option_list if "-c-" in x["code"] and x['amount'] < 0]
    b = [(x['code'], x['amount'], Option.objects.get(code=x['code']).deposit_today)
         for x in option_list if "-c-" in x["code"] and x['amount'] < 0]
    c = [(x['code'], x['amount'], Option.objects.get(code=x['code']).deposit_today)
         for x in option_list if "-c-" in x["code"] and x['amount'] > 0]
    d = [(x['code'], x['amount'], Option.objects.get(code=x['code']).deposit_today)
         for x in option_list if "-c-" in x["code"] and x['amount'] > 0]
    return a, b, c, d


def hedge_cost(future_list, option_list):
    cost = 0.
    call_option_short_pair, put_option_short_pair, \
    call_option_long_pair, put_option_long_pair = _split_option_list(future_list)

    # assume while amount positive means long lots, otherwise means short lots
    # total_call_option_long_lots = sum([abs(x[1]) for x in call_option_long_pair])
    # total_put_option_long_lots = sum([abs(x[1]) for x in put_option_long_pair])
    # total_call_option_short_lots = sum([abs(x[1]) for x in call_option_short_pair])
    # total_put_option_short_lots = sum([abs(x[1]) for x in put_option_short_pair])

    pass