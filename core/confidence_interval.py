from numpy import mean, std


def get_confidence(array):
    alpha = 0.95
    m = mean(array)  # general average
    sigma = std(array)  # standard deviation

    # confidence interval
    print('mean accuracy: ', m)
    print('standart deviation: ', sigma)
    print('confidence interval: (', m - alpha * sigma, ';', m + alpha * sigma, ')')
