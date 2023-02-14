import numpy as np
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, plot_type, width=6, line_width=0.8, label_size=12):
        self.width = width
        self.height = width / 1.618
        self.line_width = line_width
        self.label_size = label_size
        self.plot_type = plot_type
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize=self.label_size)
        plt.rc('ytick', labelsize=self.label_size)
        plt.rc('axes', labelsize=self.label_size)

    def print_size(self):
        print(self.width, self.height)

    def generate_plot(self, data, sampling_rate):
        fig, ax = plt.subplots()
        fig.subplots_adjust(left=.16, bottom=.17, right=.99, top=.97)
        if self.plot_type == 'rir_time':
            data_len = len(data)
            time = np.arange(0, data_len/sampling_rate, (1/sampling_rate)).T
            plt.plot(time,
                     data,
                     ls='solid',
                     color='k',
                     linewidth=self.line_width)
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.show()
