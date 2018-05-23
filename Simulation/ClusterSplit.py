import numpy as np
import pandas as pd
from pandas import HDFStore

RoomSize 			= 		[2.9, 2.14, 3.1]				# Room dimensions [x y] (m)
TransSeparation     =       0.05                            # Anti-source Separation distance
MonteCarloLen       =       100                             # Set MonteCarlo Iterations


print "Creating Anti-Noise Source Locations"

x                   =       np.arange(0.1, 2.9, TransSeparation)
y                   =       np.arange(0.1, 2.14, TransSeparation)
zpos                =       0.82

N = len(x)*len(y)                                           # A total combinations for x, and y

AntiNoiseLoc = np.zeros((N, 3))

i = 0
for xpos in x:
    for ypos in y:
        AntiNoiseLoc[i,:]=np.array((xpos, ypos, zpos))
        i = i+1


integer, dec    =   divmod(zpos, 1)
integer         =   int(integer)
dec             =   int(round(dec,2)*100)


print 'Total Spatial Points: ', N
print 'X is:', len(x)
print 'Y is:', len(y)


Transducers = np.zeros((MonteCarloLen, 6))

print "Creating MonteCarlo Constellation"

for i in range(MonteCarloLen):
    Sx = np.random.uniform(low=1, high=6)
    Sy = np.random.uniform(low=1, high=4)
    Sz = zpos
    Rx = np.random.uniform(low=1, high=6)
    Ry = np.random.uniform(low=1, high=4)
    Rz = zpos
    Transducers[i,:] = np.array((Sx, Sy, Sz, Rx, Ry, Rz))

TotalIterations = N*MonteCarloLen
Constellation   = np.zeros((TotalIterations, 9))

i = 0
for Transducer in Transducers:
    for AntiNoiseSrc in AntiNoiseLoc:
        Constellation[i,:] = np.append(Transducer, AntiNoiseSrc)
        i = i+1

cols                    =       ['Sx', 'Sy', 'Sz', 'Rx', 'Ry', 'Rz', 'Ax', 'Ay', 'Az']
data                    =       pd.DataFrame(Constellation, columns = cols)

hdf     =   HDFStore('Input/Configurations_Zpos_'+str(integer)+'_'+str(dec)+'.h5')
hdf.put('Config', data, format='table', data_columns=True)

print data.shape
