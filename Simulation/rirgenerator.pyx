import numpy as np
cimport numpy as np

cdef extern from "rir_generator.h":
	void computeRIR(double* imp,double c,double fs,double* rr,int nMicrophones,int nSamples,double* ss,double* LL,double* beta,char* microphone_type, int nOrder, double* angle, int isHighPassFilter)

def rir_generator(c,samplingRate,micPositions,srcPosition,LL,**kwargs):

	if type(LL) is not np.array:
		LL=np.array(LL,ndmin=2)
	if LL.shape[0]==1:
		LL=np.transpose(LL)

	if type(micPositions) is not np.array:
		micPositions=np.array(micPositions,ndmin=2)
	if type(srcPosition) is not np.array:
		srcPosition=np.array(srcPosition,ndmin=2)

	"""Passing beta"""
	cdef np.ndarray[np.double_t, ndim=2] beta = np.zeros([6,1], dtype=np.double)
	if 'beta' in kwargs:
		betaIn=kwargs['beta']
		if type(betaIn) is not np.array:
			betaIn=np.transpose(np.array(betaIn,ndmin=2))
		if (betaIn.shape[0])>1:
			beta=betaIn
			V=LL[0]*LL[1]*LL[2]
			alpha = ((1-pow(beta[0],2))+(1-pow(beta[1],2)))*LL[0]*LL[2]+((1-pow(beta[2],2))+(1-pow(beta[3],2)))*LL[1]*LL[2]+((1-pow(beta[4],2))+(1-pow(beta[5],2)))*LL[0]*LL[1]
			reverberation_time = 24*np.log(10.0)*V/(c*alpha)
			if (reverberation_time < 0.128):
				reverberation_time = 0.128
		else:
			reverberation_time=betaIn		
			if (reverberation_time != 0) :
				V=LL[0]*LL[1]*LL[2]
				S = 2*(LL[0]*LL[2]+LL[1]*LL[2]+LL[0]*LL[1])		
				alfa = 24*V*np.log(10.0)/(c*S*reverberation_time)
				if alfa>1:
					raise ValueError("Error: The reflection coefficients cannot be calculated using the current room parameters, i.e. room size and reverberation time.\n Please specify the reflection coefficients or change the room parameters.")
				beta=np.zeros([6,1])
				beta+=np.sqrt(1-alfa)
			else:
				beta=np.zeros([6,1])
	else:
			raise ValueError("Error: Specify either RT60 (ex: beta=0.4) or reflection coefficients (beta=[0.3,0.2,0.5,0.1,0.1,0.1])")
	
	"""Number of samples: Default T60 * Fs"""
	if 'nsample' in kwargs:
		nsamples=kwargs['nsample']
	else:
		nsamples=int(reverberation_time * samplingRate)

	"""Mic type: Default omnidirectional"""
	m_type='omnidirectional'
	if 'mtype' in kwargs:
		m_type=kwargs['mtype']
	if m_type is 'bidirectional':
		mtype = 'b'
	if m_type is 'cardioid':
		mtype = 'c'
	if m_type is 'subcardioid':
		mtype = 's'
	if m_type is 'hypercardioid':
		mtype = 'h'
	if m_type is 'omnidirectional':
		mtype = 'o'		

	"""Reflection order: Default -1"""
	order = -1
	if 'order' in kwargs:
		order = kwargs['order']
		if order<-1:
			raise ValueError("Invalid input: reflection order should be > -1")

	"""Room dimensions: Default 3"""
	dim=3
	if 'dim' in kwargs:
		dim=kwargs['dim']
		if dim not in [2,3]:
			raise ValueError("Invalid input: 2 or 3 dimensions expected")
		if dim is 2:
			beta[4]=0
			beta[5]=0

	"""Orientation"""
	cdef np.ndarray[np.double_t, ndim=2] angle = \
		np.zeros([2,1], dtype=np.double)
	if 'orientation' in kwargs:
		orientation=kwargs['orientation']
		if type(orientation) is not np.array:
			orientation=np.array(orientation,ndmin=2)
		if orientation.shape[1]==1:
			angle[0]=orientation[0]
		else:
			angle[0]=orientation[0,0]

			angle[1]=orientation[0,1]

	"""hp_filter enable"""
	isHighPassFilter=1
	if 'hp_filter' in kwargs:
		isHighPassFilter=kwargs['hp_filter']


	numMics=micPositions.shape[0]

	"""Create output vector"""
	cdef np.ndarray[np.double_t, ndim=2] imp = np.zeros([nsamples,numMics], dtype=np.double)

	cdef np.ndarray[np.double_t, ndim=2] roomDim = np.ascontiguousarray(LL.astype('double'), dtype=np.double)
	cdef np.ndarray[np.double_t, ndim=2] micPos = np.ascontiguousarray(np.transpose(micPositions).astype('double'), dtype=np.double)	
	cdef np.ndarray[np.double_t, ndim=2] srcPos = np.ascontiguousarray(np.transpose(srcPosition).astype('double'), dtype=np.double)	

	computeRIR(<double *>imp.data,c,samplingRate,<double *>micPos.data,numMics,nsamples,<double *>srcPos.data,<double *>roomDim.data,<double *>beta.data,mtype,order,<double *>angle.data,isHighPassFilter)
	return np.transpose(imp)
