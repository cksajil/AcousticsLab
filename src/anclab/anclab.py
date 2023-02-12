import numpy as np
from .helper import spectral_flatness


def main():
    signal = np.array(([1, 2, 3, 4, 5]))
    output = spectral_flatness(signal, sampling_freq=8000)
    print(output)


if __name__ == "__main__":
    main()
