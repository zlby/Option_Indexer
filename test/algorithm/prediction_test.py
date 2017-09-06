from algorithm.prediction.data_analyzer import sim_spot_futures as ss

def test_sport_price():
    f = ss.future_price(2000.,1.2,0.02,0.)
    print(f)
