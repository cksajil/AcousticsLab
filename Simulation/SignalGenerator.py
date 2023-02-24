import numpy as np
from scipy import signal


def GenerateSignal(T, Fs):

    n = np.arange(1, T + 1)
    wsin = np.array((0.03, 0.06, 0.09))
    ar = np.array((2, 1, 0.5))
    br = np.array((-1, -0.5, 0.1))
    narrow = np.zeros((1, T))

    for k in range(0, len(wsin)):
        narrow = (
            narrow
            + ar[k] * np.cos(np.pi * wsin[k] * n)
            + br[k] * np.sin(np.pi * wsin[k] * n)
        )

    # Wideband component with variance 0.1
    # wide 			=			np.sqrt(0.01)*np.random.randn(1, T)
    x = narrow  # +wide

    return x
