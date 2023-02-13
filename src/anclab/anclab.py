import numpy as np
from helper import spectral_flatness, generate_signal


def main():
    signal = np.array(([1, 2, 3, 4, 5]))
    output_1 = spectral_flatness(signal, sampling_freq=8000)
    print(output_1)

    output_2 = generate_signal(5, 16000)
    print(output_2)


if __name__ == "__main__":
    main()
