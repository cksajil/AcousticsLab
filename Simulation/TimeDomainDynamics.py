import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def TimeDynamics(Pd_dB, fd, Pe_dB, fe, attenuation, SourceLoc, ReceiverLoc, AntiNoiseLoc):
	
	labelsize 	= 	12
	width  		= 	5
	height 		= 	width / 1.618
	lwidth 		= 	0.9

	plt.rc('font', family='serif')
	plt.rc('text', usetex=True)
	plt.rc('xtick', labelsize=labelsize)
	plt.rc('ytick', labelsize=labelsize)
	plt.rc('axes', labelsize=labelsize)

	fig, ax = plt.subplots()
	fig.subplots_adjust(left=.20, bottom=.25, right=.96, top=.90)

	plt.plot(fd, Pd_dB, color='k', ls='dashed', linewidth=lwidth, label='ANC-OFF')

	# plt.plot(fd, Pd_dB, color='k', linewidth=lwidth)
	plt.xlim(0, 1500)
	#plt.semilogy(fd, Pd, color='r', linewidth='0.9')
	plt.plot(fe, Pe_dB, color='k', ls='solid', linewidth=lwidth, label='ANC-ON')
	#plt.semilogy(fe, Pe, color='g', linewidth='0.9')
	ax.legend()

	plt.xlabel('Frequency [Hz]')
	plt.ylabel('Power/Frequency [dB/Hz]')
	plt.savefig('TimeDynamics.pdf', dpi = 600)

	cols                    =       ['Fd', 'Pd_dB', 'Fe', 'Pe_dB']
	data                    =       pd.DataFrame(columns = cols)
	data['Fd']				=		fd
	data['Pd_dB']			=		Pd_dB
	data['Fe']				=		fe
	data['Pe_dB']			=		Pe_dB

	#print data.iloc[123]

	# data.to_csv('Results/FrequencyDynamics.csv')
	# fig.set_size_inches(width, height)
	# fig.savefig('SourceSignal.png', dpi = 600)






