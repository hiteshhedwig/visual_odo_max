import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

def get_sample_normaldist(mean, std, size=None):
    """
    The function returns a sample from a normal distribution with a given mean and standard deviation.
    
    :param mean: The mean is the average value of the distribution. It represents the central tendency
    of the data
    :param std: The standard deviation of the normal distribution. It determines the spread or
    variability of the data. A larger standard deviation means the data points are more spread out from
    the mean
    :param size: The size parameter determines the shape of the output array. If size is None (default),
    a single value will be returned. If size is an integer, a 1-D array of that length will be returned.
    If size is a tuple, an array with that shape will be returned
    :return: a sample from a normal distribution with the specified mean and standard deviation. The
    size parameter determines the shape of the returned array.
    """
    return np.random.normal(mean, std, size)


def main():
    data = get_sample_normaldist(0,1, size=(10000,))
    print(data)
    # displays gaussian distribution
    plt.hist(data, bins=30)
    plt.show()

    #prob density function - PDF 
    sns.kdeplot(data)
    plt.show()

    # compare the distribution
    sm.qqplot(data, line='45')
    plt.show()


if __name__ == '__main__':
    main()