import numpy as np
from ancplotter.ancplotter import Plot

graph_1 = Plot(plot_type='rir_time', width=6)

time = np.linspace(0., 1.0, num=1000)
data = np.sin(2*np.pi*1000*time)
graph_1.generate_plot(data, 1000)
