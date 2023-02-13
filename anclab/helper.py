from scipy import signal
import numpy as np


def spectral_flatness(data, sampling_freq, offset=1e-20):
    """
    A function to compute spectral flatness value of a signal
    """
    freq, power = signal.periodogram(data, sampling_freq)
    spectralflatness = np.exp(np.mean(np.log(power+offset)))/np.mean(power)
    return spectralflatness


def generate_signal(T, Fs):
    """
    Function to generate test signal
    """
    n = np.arange(1, T+1)
    wsin = np.array((0.03, 0.06, 0.09))
    ar = np.array((2, 1, 0.5))
    br = np.array((-1, -0.5, 0.1))
    narrow = np.zeros((1, T))
    for k in range(0, len(wsin)):
        narrow += ar[k]*np.cos(np.pi*wsin[k]*n)+br[k]*np.sin(np.pi*wsin[k]*n)
    wide = np.sqrt(0.01)*np.random.randn(1, T)
    x = narrow+wide
    return x
