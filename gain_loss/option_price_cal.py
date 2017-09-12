import QuantLib as ql
# from option.models import *
# import numpy as np
from gain_loss.history_vol import *
# import datetime
# import time as tm

# maturity_date = ql.Date(15, 1, 2016)
# spot_price = 127.62
# strike_price = 130
# volatility = 0.20 # the historical vols or implied vols
# dividend_rate =  0
# option_type = ql.Option.Call
#
# risk_free_rate = np.log(1.03)
# day_count = ql.Actual365Fixed()
# calendar = ql.China()
#
# calculation_date = ql.Date(8, 5, 2015)
# ql.Settings.instance().evaluationDate = calculation_date
#
# payoff = ql.PlainVanillaPayoff(option_type, strike_price)
# settlement = calculation_date
#
# am_exercise = ql.AmericanExercise(settlement, maturity_date)
# american_option = ql.VanillaOption(payoff, am_exercise)
#
#
# spot_handle = ql.QuoteHandle(
#     ql.SimpleQuote(spot_price)
# )
# flat_ts = ql.YieldTermStructureHandle(
#     ql.FlatForward(calculation_date, risk_free_rate, day_count)
# )
# dividend_yield = ql.YieldTermStructureHandle(
#     ql.FlatForward(calculation_date, dividend_rate, day_count)
# )
# flat_vol_ts = ql.BlackVolTermStructureHandle(
#     ql.BlackConstantVol(calculation_date, calendar, volatility, day_count)
# )
# bsm_process = ql.BlackScholesMertonProcess(spot_handle,
#                                            dividend_yield,
#                                            flat_ts,
#                                            flat_vol_ts)
#
# steps = 2000
# binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
# american_option.setPricingEngine(binomial_engine)
# print (american_option.NPV())

# def binomial_price(option, bsm_process, steps):
#     binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
#     option.setPricingEngine(binomial_engine)
#     return option.NPV()

def get_option_price(code, time, steps, price = -1, volat = -1):
    #time: 未来时间
    #price: 未来期货价格
    option_code = code
    future_code = option_code.split('-')[0]

    d_day = Future.objects.get(code=future_code).delivery_day
    maturity_date = ql.Date(d_day.day, d_day.month, d_day.year)
    calculation_date = ql.Date(time.day, time.month, time.year)
    if price <= 0:
        spot_price = FutureTreadingData.objects.get(future=future_code, time=time).close_price
    else:
        spot_price = price
    strike_price = int(option_code.split('-')[-1])
    # volatility = history_vol(code=code, day=datetime.datetime(time.year, time.month, time.day))   #to be change
    volatility = volat
    if volatility <= 0:
        volatility = history_vol(option_code)

    dividend_rate = 0
    option_type = ql.Option.Call

    risk_free_rate = np.log(1.03)
    day_count = ql.Actual365Fixed()
    calendar = ql.China()

    # time1 = tm.clock()

    ql.Settings.instance().evaluationDate = calculation_date

    payoff = ql.PlainVanillaPayoff(option_type, strike_price)
    settlement = calculation_date


    am_exercise = ql.AmericanExercise(settlement, maturity_date)
    american_option = ql.VanillaOption(payoff, am_exercise)

    spot_handle = ql.QuoteHandle(
        ql.SimpleQuote(spot_price)
    )
    flat_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, risk_free_rate, day_count)
    )
    dividend_yield = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, dividend_rate, day_count)
    )
    flat_vol_ts = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(calculation_date, calendar, volatility, day_count)
    )
    bsm_process = ql.BlackScholesMertonProcess(spot_handle,
                                               dividend_yield,
                                               flat_ts,
                                               flat_vol_ts)

    binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
    american_option.setPricingEngine(binomial_engine)

    # print(american_option.NPV())
    #
    # time2 = tm.clock()
    # print(time2 - time1)
    return american_option.NPV()