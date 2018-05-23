#####################################################################################################
print "Loading Libraries"

import time
import numpy as np
import pandas as pd
from RIRGenKernel import ComputeRIRs
from MyFxLMS import ANCInAction
from SignalGenerator import GenerateSignal
from multiprocessing import Pool
from PerformanceMetrics import metrics

#####################################################################################################

t1 = time.time()

print "Setting Simulation Parameters"

# Parameter Settings
c 					= 		343								# Sound velocity (m/s)
Fs 					= 		2000.0							# Sample frequency (samples/s)
RoomSize 			= 		[6, 4, 3]						# Room dimensions [x y] (m)
#SourceLoc 			= 	    np.array((3, 2, 1.5))			# Source position [x y z] (m)
#ReceiverLoc 		= 		np.array((1, 3, 1.5))     		# Receiver positions [x y] (m)
TransSeparation     =       0.31                            # Anti-source Separation distance
beta                =       0.4                             # Reverberation Time
nsample 			= 		1000   						    # Number of samples
mtype 				= 		'omnidirectional'				# Type of microphone
order 				= 		-1								# -1 equals maximum reflection order!
dim 				= 		3								# Room dimension
orientation 		= 		0								# Microphone orientation (rad)
hp_filter 			= 		1								# Enable high-pass filter
T                   =       100000                          # Normalised Simulation Time
L 					= 		256							    # Set Filter Length
mu                  =       0.0001                          # Set Learning Rate
MonteCarloLen       =       100                             # Set MonteCarlo Iterations


#####################################################################################################

print "Creating Anti-Noise Source Locations"

x = np.arange(0.1, 6, TransSeparation)
y = np.arange(0.1, 4, TransSeparation)
z = np.arange(0.1, 3, TransSeparation)


N = len(x)*len(y)*len(z) # A total of 2600 combinations for x, y and z


AntiNoiseLoc = np.zeros((N, 3))
i = 0
for zpos in z:
    for xpos in x:
        for ypos in y:
            AntiNoiseLoc[i,:]=np.array((xpos, ypos, zpos))
            i = i+1

#####################################################################################################

Transducers = np.zeros((MonteCarloLen, 6))


for i in range(MonteCarloLen):
    Sx = np.random.uniform(low=1, high=6)
    Sy = np.random.uniform(low=1, high=4)
    Sz = np.random.uniform(low=1, high=3)
    Rx = np.random.uniform(low=1, high=6)
    Ry = np.random.uniform(low=1, high=4)
    Rz = np.random.uniform(low=1, high=3)
    Transducers[i,:] = np.array((Sx, Sy, Sz, Rx, Ry, Rz))

TotalIterations = N*MonteCarloLen
Constellation   = np.zeros((TotalIterations, 9))

i = 0
for Transducer in Transducers:
    for AntiNoiseSrc in AntiNoiseLoc:
        Constellation[i,:] = np.append(Transducer, AntiNoiseSrc)
        i = i+1


#np.savetxt('config.txt', Constellation, delimiter=',')

#####################################################################################################

print "Writing Experiment Log"

with open("log.txt", "w") as logger:
    logger.write("The experiment configuration were\n"
    			 "\nSampling Rate      					: 		%s" %Fs+
    			 "\nSound Speed        					: 		%s" %c+
    			 "\nRoom size          					: 		%s" %RoomSize+
    			 "\nRIR Samples length 					: 		%s" %nsample+
    			 "\nMicrophone Type        				: 		%s" %mtype+
    			 "\nBeta               					: 		%s" %beta+
    			 "\nNumber of Reflections  				: 		%s" %order+
    			 "\nSimulation Dimentions  				: 		%s" %dim+
    			 "\nMicrophone Orientation  			: 		%s" %orientation+
    			 "\nHigh Pass Filter        			: 		%s" %hp_filter+
    			 "\nNormalised Simulation Time        	: 		%s" %T+
    			 "\nFilter length        				: 		%s" %L+
    			 "\nLearning Rate        				: 		%s" %mu+
                 "\nAnti Source Separation              :       %s" %TransSeparation+
                 "\nMonte Carlo length                  :       %s" %MonteCarloLen+
    			 "\n\nConstellation Locations		    : 		%s" %Constellation)

#####################################################################################################

print "Generating Input Signal"

x               =   GenerateSignal(T, Fs)

#####################################################################################################

print "Started Parallel Processing"

def ParallelProcessing(location):
    SourceLoc       = location[0:3]
    ReceiverLoc     = location[3:6]
    Antilocation    = location[6:9]
  
    P, S            =   ComputeRIRs(c,Fs,ReceiverLoc,SourceLoc,Antilocation,RoomSize,beta,nsample,mtype,order,dim,orientation,hp_filter)
    e_cont, Yd  	=  	ANCInAction(P, S, x, T, L, mu)
    Pd_dB, fd, Pe_dB, fe, EstimatedAttenuation, components =   metrics(e_cont, Yd, Fs, T)
 
    features              =   np.append(location, EstimatedAttenuation)
    features              =   np.append(features, components)
    return features

P 		                  =   Pool()
result                    =   P.map(ParallelProcessing, Constellation)

#####################################################################################################

print "Saving Final Result"


cols                    =       ['Sx', 'Sy', 'Sz', 'Rx', 'Ry', 'Rz', 'Ax', 'Ay', 'Az', 'Attenuation', '30Hz', '60Hz', '90Hz']
data                    =       pd.DataFrame(result, columns = cols)
data.to_csv('Results/MasterDataSet.csv')

#####################################################################################################

t2 = time.time()

m, s = divmod(t2-t1, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)

print "Done Simulation in %d Days, %d Hours, %02d Minutes, %02d Seconds" % (d, h, m, s)




####################################################################################################
