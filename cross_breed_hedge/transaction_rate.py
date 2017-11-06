import statsmodels.api as sm

'''
return y/x 手数比
'''
def OLS(diffx, diffy):
    if len(diffx) == len(diffy):
        x = sm.add_constant(diffx)
        model = sm.OLS(diffy, x)
        result = model.fit()
        return result.params[1]
    else:
        return None

def get_diff(list):
    result_list = []
    for i in range(1, len(list)):
        result_list.append(list[i] - list[i-1])

    return result_list