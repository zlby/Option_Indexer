
from option.models import *
import numpy as np

# maturity_date = ql.Date(15, 1, 2016)
# spot_price = 127.62
# strike_price = 130
# volatility = 0.20 # the historical vols or implied vols
# dividend_rate =  0.0163
# option_type = ql.Option.Call
#
# risk_free_rate = 0.001
# day_count = ql.Actual365Fixed()
# calendar = ql.UnitedStates()
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
# eu_exercise = ql.EuropeanExercise(maturity_date)
# european_option = ql.VanillaOption(payoff, eu_exercise)
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
# steps = 200
# binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
# american_option.setPricingEngine(binomial_engine)
# print (american_option.NPV())
#
# def binomial_price(option, bsm_process, steps):
#     binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
#     option.setPricingEngine(binomial_engine)
#     return option.NPV()
#
# steps = range(5, 200, 1)
# eu_prices = [binomial_price(european_option, bsm_process, step) for step in steps]
# am_prices = [binomial_price(american_option, bsm_process, step) for step in steps]
# # theoretican European option price
# european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
# bs_price = european_option.NPV()
#
#
#
# plt.plot(steps, eu_prices, label="European Option", lw=2, alpha=0.6)
# plt.plot(steps, am_prices, label="American Option", lw=2, alpha=0.6)
# plt.plot([5,200],[bs_price, bs_price], "r--", label="BSM Price", lw=2, alpha=0.6)
# plt.xlabel("Steps")
# plt.ylabel("Price")
# plt.ylim(6.7,7)
# plt.title("Binomial Tree Price For Varying Steps")
# plt.legend()
#
# plt.show()


def history_vol(code):
    option_code = code
    future_code = option_code.split('-')[0]
    query_set = DayFutureTreadingData.objects.filter(future=future_code).order_by('-time')
    query_list = []
    for i in range(31):
        query_list.insert(0, query_set[i].close_price)
    log_list = []
    log_sum = 0
    for i in range(30):
        log_list.append(np.log(query_list[i+1] / query_list[i]))
        log_sum += log_list[i]
    log_avg = log_sum / 30

    sqr_sum = 0
    for i in range(30):
        sqr_sum += np.power(log_list[i] - log_avg, 2)

    return np.sqrt(252 / 29 * sqr_sum)

