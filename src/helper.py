from scipy import signal
import numpy as np


def spectral_flatness(data, sampling_freq, offset=1e-20):
    """
    A function to compute spectral flatness value of a signal
    """
    freq, power = signal.periodogram(data, sampling_freq)
    spectralflatness = np.exp(np.mean(np.log(power+offset)))/np.mean(power)
    return spectralflatness
