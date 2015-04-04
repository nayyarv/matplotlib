datsize = 10000
__author__ = 'varunnayyar'

import numpy as np
from matplotlib import pyplot as plt, mlab
plt.style.use('ggplot')


def min6decorator(func):
    def inner(*args, **kwargs):
        return max(func(*args, **kwargs), 6)
    return inner

def sturges(x):
    # using Sturges estimator
    print np.log2(x.size)
    return np.ceil(np.log2(x.size)) + 1

def rice(x):
    return np.ceil(2 * len(x) ** (1.0/3))


def sturice(x):
    return np.ceil((rice(x) + sturges(x))/2)

def scott(x):
    h = 3.5 * x.std() * x.size **(-1.0/3)
    if h>0:
        return np.ceil(x.ptp()/h)
    return 1

def mad(data, axis=None):
    return np.median(np.absolute(data - np.median(data, axis)), axis)

def FD(x):
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    if iqr > 0:
        return np.ceil(x.ptp()/(2 * iqr * x.size**(-1.0/3)))
    elif iqr == 0:
        return 10 # fix
    return 1

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x1 = mu + sigma * np.random.randn(datsize/2)
x2 = 80 + 5 * np.random.randn(datsize/2)
x = np.hstack((x1, x2))


autoMethods = [sturges, rice, scott, sturice]

num_bins = [10, 50] + map(lambda method: method(x), autoMethods)
bindesc = ["default", "manual"] + map(lambda method: method.__name__, autoMethods)

plt.figure(tight_layout=True, figsize=(14,7))

# exit()
for i in range(len(bindesc)):
    binChoice = num_bins[i]
    desc = bindesc[i]
    plt.subplot(2,3,i+1)
    # the histogram of the data
    n, bins, patches = plt.hist(x, binChoice, normed=1, facecolor = 'green', alpha=0.5)
    plt.xlabel('X axis')
    plt.ylabel('Probability')
    plt.title(r'method = {1}, nbins = {0}'.format(binChoice, desc))

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
plt.show()
