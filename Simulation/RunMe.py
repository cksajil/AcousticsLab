#####################################################################################################
print("Loading Libraries")

import time
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from MyFxLMS import ANCInAction
from multiprocessing import Pool
from RIRGenKernel import ComputeRIRs
from PerformanceMetrics import metrics
from SignalGenerator import GenerateSignal

#####################################################################################################

print("Setting Simulation Parameters")

c = 343  # Sound velocity (m/s)
Fs = 12000.0  # Sample frequency (samples/s)
RoomSize = [2.9, 2.14, 3.1]  # Room dimensions [x y] (m)
SourceLoc = np.array((1.4, 2.0, 0.82))  # Source position [x y z] (m)
ReceiverLoc = np.array((1.4, 1.0, 0.82))  # Receiver positions [x y] (m)
beta = 0.3942  # Reverberation Time
nsample = 5000  # Number of samples
mtype = "omnidirectional"  # Type of microphone
order = -1  # -1 equals maximum reflection order!
dim = 3  # Room dimension
orientation = 0  # Microphone orientation (rad)
hp_filter = 1  # Enable high-pass filter
T = 24000  # Normalised Simulation Time
L = 800  # Set Filter Length
mu = 0.000001  # Set Learning Rate

#####################################################################################################

print("Reading Constellations")

zpos = 0.82
positions = pd.read_excel(
    open("MeasurementSheet_EditedWithDiffCol.xlsx", "rb"), index=False
)
positions = positions.values

#####################################################################################################

print("Generating Input Signal")

x = GenerateSignal(T, Fs)

#####################################################################################################

t1 = time.time()


def ParallelProcessing(location):
    Antilocation = location[1:4]

    P, S = ComputeRIRs(
        c,
        Fs,
        ReceiverLoc,
        SourceLoc,
        Antilocation,
        RoomSize,
        beta,
        nsample,
        mtype,
        order,
        dim,
        orientation,
        hp_filter,
    )
    e_cont, Yd = ANCInAction(P, S, x, T, L, mu)
    Pd_dB, fd, Pe_dB, fe, EstimatedAttenuation, components = metrics(e_cont, Yd, Fs, T)

    features = np.append(Antilocation, EstimatedAttenuation)
    features = np.append(features, components)
    return features


P = Pool()
result = P.map(ParallelProcessing, positions)


# #####################################################################################################

print("Saving Final Result")

cols = ["Ax", "Ay", "Az", "Attenuation", "30Hz", "60Hz", "90Hz"]
data = pd.DataFrame(result, columns=cols)
writer = ExcelWriter("Results/Results__Zpos_0_82.xlsx")

data.to_excel(writer, "Sheet1")
writer.save()

#####################################################################################################

t2 = time.time()

m, s = divmod(t2 - t1, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)

print("Done Simulation in %d Days, %d Hours, %02d Minutes, %02d Seconds" % (d, h, m, s))

# ####################################################################################################
