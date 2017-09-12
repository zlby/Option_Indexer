import numpy as np

def get_coherence_rate(spot_data_list, future_data_list):
    npl1 = np.asarray(spot_data_list)
    npl2 = np.asarray(future_data_list)

    var1 = np.sqrt(np.var(npl1))
    var2 = np.sqrt(np.var(npl2))

    cov = np.cov(npl1, npl2)[0][1]

    return (cov/(var1 * var2))