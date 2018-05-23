import numpy as np
import pandas as pd
from pandas import ExcelWriter

RoomSize 			= 		[2.9, 2.14, 3.1]				# Room dimensions [x y] (m)
TransSeparation     =       0.05                            # Anti-source Separation distance

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

Constellation   = np.zeros((N, 9))

Transducers     = np.array((1.4, 2.0, 0.82, 1.4, 1.0, 0.82))

i = 0
for AntiNoiseSrc in AntiNoiseLoc:
    Constellation[i,:] = np.append(Transducers, AntiNoiseSrc)
    i = i+1

cols                    =       ['Sx', 'Sy', 'Sz', 'Rx', 'Ry', 'Rz', 'Ax', 'Ay', 'Az']
data                    =       pd.DataFrame(Constellation, columns = cols)

writer                  =       ExcelWriter('Input/Inputs__Zpos_0_82.xlsx')

data.to_excel(writer,'Sheet1')
writer.save()