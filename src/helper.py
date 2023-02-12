from scipy import signal
import numpy as np


def SpectralFlatness(x, Fs, offset=1e-20):
    f, Pxx_den = signal.periodogram(x, Fs)
    spectralflatness = np.exp(np.mean(np.log(Pxx_den+offset)))/np.mean(Pxx_den)
    return spectralflatness
