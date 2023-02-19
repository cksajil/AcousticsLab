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

    def rir_plot(self, data, sampling_rate):
        """
        Function to plot given room impulse response
        """
        fig, ax = plt.subplots()
        fig.subplots_adjust(left=.16, bottom=.17, right=.99, top=.97)
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

    def secondary_path_graphs(self, Sw, Shw):
        """
        Function to plot secondary path impulse response and its estimate
        """
        fig, ax = plt.subplots()
        fig.subplots_adjust(left=.16, bottom=.17, right=.99, top=.97)

        plt.subplot(2, 1, 1)
        plt.stem(Sw, markerfmt='*', label='Coefficients of Sz')
        plt.ylabel('Amplitude')
        plt.xlabel('Numbering of filter tap')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.stem(Shw, markerfmt='*', label='Coefficients of Shz')
        plt.ylabel('Amplitude')
        plt.xlabel('Numbering of filter tap')
        plt.legend()
        plt.show()

    def error_plot(self, error_sig):
        """
        A function to plot ANC cancelled error signal
        """
        fig, ax = plt.subplots()
        fig.subplots_adjust(left=.16, bottom=.17, right=.99, top=.97)
        plt.plot(error_sig, label='error signal')
        plt.ylabel('Amplitude')
        plt.xlabel('Time (s)')
        plt.legend()
        plt.show()
