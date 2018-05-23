#####################################################################################################
print "Loading Libraries"

import time
import numpy as np
import pandas as pd
from pandas import read_hdf
from pandas import ExcelWriter
from RIRGenKernel import ComputeRIRs
from MyFxLMS import ANCInAction
from SignalGenerator import GenerateSignal
from multiprocessing import Pool
from PerformanceMetrics import metrics


#####################################################################################################

print "Setting Simulation Parameters"

c 					= 		343								# Sound velocity (m/s)
Fs 					= 		12000.0							# Sample frequency (samples/s)
RoomSize 			= 		[2.9, 2.14, 3.1]						# Room dimensions [x y] (m)
TransSeparation     =       0.05                            # Anti-source Separation distance
beta                =       0.3942                             # Reverberation Time
nsample 			= 		5000   						    # Number of samples
mtype 				= 		'omnidirectional'				# Type of microphone
order 				= 		-1								# -1 equals maximum reflection order!
dim 				= 		3								# Room dimension
orientation 		= 		0								# Microphone orientation (rad)
hp_filter 			= 		1								# Enable high-pass filter
T                   =       24000                          # Normalised Simulation Time
L 					= 		800							    # Set Filter Length
mu                  =       0.000001                          # Set Learning Rate
MonteCarloLen       =       100                             # Set MonteCarlo Iterations

#####################################################################################################

print "Reading Constellations"

Constellation = read_hdf('Input/Configurations_Zpos_0_82.h5','Config')
Constellation = Constellation.iloc[57400:114800,:]

Clusters    =   4
Total       =   Constellation.shape[0]
cluster     =   0


Constellation = Constellation.iloc[cluster*(Total/Clusters):(cluster+1)*(Total/Clusters),:]
Constellation = Constellation.values

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
                 "\nMonte Carlo length                  :       %s" %MonteCarloLen)

#####################################################################################################

print "Generating Input Signal"

x               =   GenerateSignal(T, Fs)

#####################################################################################################

t1 = time.time()

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
writer                  =       ExcelWriter('Results/Results__Zpos_0.82_Cluster_quarter_'+str(cluster)+'.xlsx')


data.to_excel(writer,'Sheet1')
writer.save()

#####################################################################################################

t2 = time.time()

m, s = divmod(t2-t1, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)

print "Done Simulation in %d Days, %d Hours, %02d Minutes, %02d Seconds" % (d, h, m, s)

####################################################################################################
