from scipy import signal
import numpy as np

def metrics(error, Yd, Fs, T):

	# fd, Pd 	= 	signal.welch(Yd[T-T/3:], Fs, nperseg=4096, nfft=8192)
	# fe, Pe 	= 	signal.welch(error[T-T/3:], Fs, nperseg=4096, nfft=8192)

	# Pd_dB 	= 	10*np.log10(Pd)
	# Pe_dB 	= 	10*np.log10(Pe)

	# components 			 = [Pd_dB[123]-Pe_dB[123], Pd_dB[246]-Pe_dB[246], Pd_dB[369]-Pe_dB[369]]
	# EstimatedAttenuation = 10*np.log10(np.var(Yd)/np.var(error[T-T/3:]))

	# return Pd_dB, fd, Pe_dB, fe, EstimatedAttenuation, components
	ANCRed = 10*np.log10(np.sum(np.square(Yd))/np.sum(np.square(error)))
	return ANCRed
