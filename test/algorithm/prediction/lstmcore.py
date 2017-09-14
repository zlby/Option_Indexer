from algorithm.prediction.lstmcore import LstmModel

def runtest():
    import numpy as np
    axs = np.arange(0, 20000, dtype=np.float32) * 0.005
    series = np.cos(axs)
    test_object = LstmModel(series)
    test_object.train_till_series_end()
    import pylab as plt
    count = test_object.predication.shape[0] - 1
    plt.plot(axs[:count], series[:count], "b")
    plt.plot(axs[:count], test_object.predication[0:count], "r--")
    plt.show()

if __name__ == "__main__":
    runtest()