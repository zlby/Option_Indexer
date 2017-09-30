import numpy as np
from sklearn.cross_decomposition import CCA

def get_coherence_rate(spot_data_list, future_data_list):
    npl1 = np.asarray(spot_data_list)
    npl2 = np.asarray(future_data_list)

    var1 = np.sqrt(np.var(npl1))
    var2 = np.sqrt(np.var(npl2))

    cov = np.cov(npl1, npl2)[0][1]

    return (cov/(var1 * var2))


def canonical_correlation_analysis(list_a, list_b, list_y):
    X = []
    Y = []
    if len(list_a) != len(list_b) or len(list_b) != len(list_y):
        return None

    for i in range(len(list_a)):
        X.append([list_a[i], list_b[i]])
        Y.append(list_y[i])


    cca = CCA(n_components=1)
    X_c, Y_c = cca.fit_transform(X, Y)
    result = np.corrcoef(X_c.T, Y_c.T)[0, 1]

    print(np.corrcoef(X_c.T, Y_c.T))
    return result