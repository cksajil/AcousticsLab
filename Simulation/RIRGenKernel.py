# Import Libraries
import numpy as np
import rirgenerator as RG

###########################################################################################################

def ComputeRIRs(c,Fs,ReceiverLoc,SourceLoc,AntiNoiseLoc,RoomSize,beta,nsample,mtype,order,dim,orientation,hp_filter):

	# Compute the Primary Path RIR
	h = RG.rir_generator(c, Fs, ReceiverLoc , SourceLoc, RoomSize , beta=beta, nsample=nsample, mtype=mtype, order=order, dim=dim, orientation=orientation, hp_filter=hp_filter)
	h = h[0]
	# Normalise the Array
	hnorm = h / np.linalg.norm(h)
	h = hnorm


	# Compute the Secondary Path RIR
	g = RG.rir_generator(c, Fs, ReceiverLoc , AntiNoiseLoc, RoomSize , beta=beta, nsample=nsample, mtype=mtype, order=order, dim=dim, orientation=orientation, hp_filter=hp_filter)
	g = g[0]
	# Normalise the Array
	gnorm = g / np.linalg.norm(g)
	g = gnorm

	return h,g
###########################################################################################################
