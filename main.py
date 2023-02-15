import numpy as np
from ancplotter.ancplotter import Plot
import pyroomacoustics as pra

graph_1 = Plot(plot_type='rir_time', width=6)
time = np.linspace(0., 1.0, num=1000)
data = np.sin(2*np.pi*1000*time)
# graph_1.rir_plot(data, 1000)

rt60_tgt = 0.3
room_dim = [10, 7.5, 3.5]
e_absorption, max_order = pra.inverse_sabine(rt60_tgt,
                                             room_dim)

room = pra.ShoeBox(room_dim,
                   fs=8000,
                   materials=pra.Material(e_absorption),
                   max_order=max_order)

room.add_source([2.5, 3.73, 1.76],
                signal=data,
                delay=0.5)

room.add_source([1.5, 4, 2],
                signal=data,
                delay=0.5)

mic_locs = np.c_[[6.3, 4.87, 1.2]]

room.add_microphone_array(mic_locs)
room.simulate()

graph_1.secondary_path_graphs(room.rir[0][0],
                              room.rir[0][1])
