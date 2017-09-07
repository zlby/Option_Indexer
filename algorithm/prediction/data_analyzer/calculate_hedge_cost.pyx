# encoding = utf-8
cdef:
    int CODE = 0
    int AMOUNT = 1
    int DEPOSIT = 2
    int PRICE = 3
    float _calculate_sum_cost(list lots, list deposit, int size):
        cdef float _sum = 0.
        for i in range(0,size):
            _sum += lots[i] * deposit[i]
        return _sum

    float _calculate_lots_cost(int call_option_short_total_lots,
                               int call_option_long_total_lots,
                               int put_option_short_total_lots,
                               int put_option_long_total_lots):
        return (call_option_long_total_lots + call_option_short_total_lots
               + put_option_long_total_lots + put_option_short_total_lots) * 1.0

    float _calculate_call_option_trade_lots_cost(list call_option_lots_amount, list recent_call_option_price,
                                                 list put_option_lots_amount, list recent_put_option_price, int size):
        cdef float _sum = 0.
        for i in range(0, size):
            _sum += (call_option_lots_amount[i] * recent_call_option_price[i]
                 + put_option_lots_amount[i] * recent_put_option_price[i]) * 10.0
        return _sum

    float _calculate_future_cost(int future_short_lots, int future_long_lots):
        return (future_long_lots * future_short_lots) * 1.5

    float _hedge_cost(list c_l, list c_s, list p_l, list p_s, list f_l, list f_s):
        # Assume Amount is always positive , whether it's long lot or short lot.
        # fixme: when *amount* is belong to a short lots, apply abs function on it.
        cdef float _sum = 0.
        _sum += _calculate_sum_cost([x[AMOUNT] for x in c_s], [x[DEPOSIT] for x in c_s], len(c_l))
        _sum += _calculate_sum_cost([x[AMOUNT] for x in p_s], [x[DEPOSIT] for x in p_s], len(p_s))
        _sum += _calculate_lots_cost(
            sum([x[AMOUNT] for x in c_l]),
            sum([x[AMOUNT] for x in p_s]),
            sum([x[AMOUNT] for x in p_l]),
            sum([x[AMOUNT] for x in c_s])
        )

        _sum -= _calculate_call_option_trade_lots_cost(
            [x[AMOUNT] for x in c_s], [x[PRICE] for x in c_s],
            [x[AMOUNT] for x in p_s], [x[PRICE] for x in p_s],
            len(c_s)
        )
        _sum += _calculate_call_option_trade_lots_cost(
            [x[AMOUNT] for x in c_l], [x[PRICE] for x in c_l],
            [x[AMOUNT] for x in p_l], [x[PRICE] for x in p_l],
            len(c_s)
        )
        _sum += _calculate_sum_cost([x[AMOUNT] for x in f_s], [x[DEPOSIT] for x in f_s], len(f_s))
        _sum += _calculate_sum_cost([x[AMOUNT] for x in f_l], [x[DEPOSIT] for x in f_l], len(f_l))
        _sum += _calculate_future_cost(sum([x[AMOUNT] for x in f_s]), sum(x[AMOUNT] for x in f_l))
        return _sum

def hedge_cost(list c_l, list c_s, list p_l, list p_s, list f_l, list f_s):
    return _hedge_cost( c_l,  c_s,  p_l,  p_s,  f_l,  f_s)