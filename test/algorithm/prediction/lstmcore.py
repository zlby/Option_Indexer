from algorithm.prediction.lstmcore import LstmModel
import pymysql as db

def runtest():
    import numpy as np
    database = db.connect("localhost","root","root","option_indexer")
    csr = database.cursor()
    csr.execute("select price from option_spot")
    entrys = csr.fetchall()
    series = np.asarray([a[0] for a in entrys])
    axs = np.arange(0., 100., 0.1,dtype=np.float32)
    # series = np.sin(axs)
    test_object = LstmModel(series)
    test_object.train_till_series_end()
    import pylab as plt
    prd = test_object.get_prediction_list()
    count = prd.shape[0] - 1
    plt.plot(series[:count], "b")
    plt.plot(prd[0:count], "r")
    plt.show()
    csr.close()
    database.close()

def longPredTest():
    import numpy as np
    database = db.connect("localhost","root","root","option_indexer")
    csr = database.cursor()
    csr.execute("select price from option_spot")
    entrys = csr.fetchall()
    series = np.asarray([a[0] for a in entrys])
    test_object = LstmModel(series)
    test_object.train_till_series_end()
    _ = test_object.predict(30)
    import pylab as plt
    plt.plot(test_object.get_prediction_list())
    plt.plot(series, 'r')
    plt.show()
    _ = test_object.predict(40)
    print("second prediction")
    csr.close()
    database.close()

if __name__ == "__main__":
    longPredTest()
