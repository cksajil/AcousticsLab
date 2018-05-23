#####################################################################################################
print "Loading Libraries"

import time
import numpy as np
from Designer import ANCGraphs
from MyFxLMS import ANCInAction
from PerformanceMetrics import metrics
from RIRGenKernel import ComputeRIRs
from SignalGenerator import GenerateSignal
from TimeDomainDynamics import TimeDynamics

#####################################################################################################

c 					= 		343									# Sound velocity (m/s)
Fs 					= 		12000.0								# Sample frequency (samples/s)
RoomSize 			= 		[2.9, 2.14, 3.1]					# Room dimensions [x y] (m)
SourceLoc 			= 	    np.array((1.4, 2.0, 0.82))			# Source position [x y z] (m)
ReceiverLoc 		= 		np.array((1.4, 1.0, 0.82))     		# Receiver positions [x y] (m)
AntiNoiseLoc        =       np.array((2.4, 0.4, 0.82))

beta         		=   	0.3942							# Reverberation Time
nsample 			= 		5000   							# Number of samples
mtype 				= 		'omnidirectional'				# Type of microphone
order 				= 		-1								# -1 equals maximum reflection order!
dim 				= 		3								# Room dimension
orientation 		= 		0								# Microphone orientation (rad)
hp_filter 			= 		1								# Enable high-pass filter
T                   =       24000                          	# Normalised Simulation Time
L 					= 		800							    # Set Filter Length
mu                  =       0.00001                        	# Set Learning Rate

###########################################################################################################
print "Generating Input Signal"

x               	=   GenerateSignal(T, Fs)
###########################################################################################################
t1 = time.time()

print "Computing RIRs"

P, S            	=   ComputeRIRs(c,Fs,ReceiverLoc,SourceLoc,AntiNoiseLoc,RoomSize,beta,nsample,mtype,order,dim,orientation,hp_filter)

print "Simulating ANC"

error, Yd  	=  	ANCInAction(P, S, x, T, L, mu)

# Pd_dB, fd, Pe_dB, fe, attenuation, components	= 	metrics(error, Yd, Fs, T)
# print "Estimated Attenuation is : ", attenuation, components

ANCRed = metrics(error, Yd, Fs, T)


###########################################################################################################
# Generate Dynamic Power Spectral Density Graphs

# TimeDynamics(Pd_dB, fd, Pe_dB, fe, attenuation, SourceLoc, ReceiverLoc, AntiNoiseLoc)
# RIRTimeDomain(P, Fs)
# EnergyDecayCurve(P, Fs, S)
# ANCGraphs(ANCRed, error, Yd)

###########################################################################################################

t2 = time.time()

m, s = divmod(t2-t1, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)

print "Done Simulation in %d Days, %d Hours, %02d Minutes, %02d Seconds" % (d, h, m, s)
###########################################################################################################