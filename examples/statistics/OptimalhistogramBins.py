__author__ = 'varunnayyar'

import numpy as np
from matplotlib import pyplot as plt, mlab
plt.style.use('ggplot')


def min10decorator(func):
    def inner(*args, **kwargs):
        return max(func(*args, **kwargs), 10)
    return inner

def sturges(x):
    # using Sturges estimator
    print np.log2(x.size)
    return np.ceil(np.log2(x.size)) + 1

def rice(x):
    return np.ceil(2 * len(x) ** (1.0/3))


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
x = mu + sigma * np.random.randn(10000)

autoMethods = [sturges, rice, scott, FD]

num_bins = [10, 50] + map(lambda y: y(x), autoMethods)
bindesc = ["default", "manual"] + map(lambda y: y.__name__, autoMethods)

print num_bins
print bindesc


exit()
for binChoice, desc in zip(num_bins, bindesc):
    # the histogram of the data
    n, bins, patches = plt.hist(x, binChoice, normed=1, facecolor='green', alpha=0.5)
    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, '--')
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title(r'$N(100, 15^2)$, nbins = {}, method = {}'.format(binChoice, desc))

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.show()
