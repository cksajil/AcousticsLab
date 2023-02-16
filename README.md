# AcousticsLab (Ongoing Project)
A Python module for simulating Active Noise Control (ANC) experiments


**Python Version**
``` 
Python 3.9.12
```

### Setup

*Install virtual environment*
```console
python -m pip install --user virtualenv
```

*Create a new virtual environment*
```console
python -m venv venv
```

*Activating virtual environment*
```console
source venv/bin/activate
```

*Upgrade PIP*
```console
python -m pip install --upgrade pip
```

*Installing dependencies*
```console
python -m pip install -r requirements.txt
```

### How to run
```python
import numpy as np
from ancplotter.ancplotter import Plot
import pyroomacoustics as pra

# Set room parameters
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

#Simulate
room.simulate()

graph_1.secondary_path_graphs(room.rir[0][0],
                              room.rir[0][1])
```
