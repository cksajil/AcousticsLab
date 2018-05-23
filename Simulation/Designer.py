import numpy as np
import matplotlib.pyplot as plt

width  		= 	6
height 		= 	width / 1.618
lwidth 		= 	0.8
labelsize 	= 	12

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize = labelsize)
plt.rc('ytick', labelsize = labelsize)
plt.rc('axes', labelsize  = labelsize)


def RIRTimeDomain(P, Fs, width = width, height = height, lwidth = 0.8, labelsize = 10):
	fig1, ax = plt.subplots()
	fig1.subplots_adjust(left=.16, bottom=.17, right=.99, top=.97)

	Lp = len(P)
	Tp = np.arange(0, Lp/Fs, (1/Fs)).T
	plt.plot(Tp, P, ls='solid', color = 'k', linewidth=lwidth)
	plt.xlabel('$Time(s)$')
	plt.ylabel('$Amplitude$')
	plt.show()

	# fig1.set_size_inches(width, height)
	# fig1.savefig('RIRTimeDomain.pdf')

def EnergyDecayCurve(P, Fs, S=None, width = width, height = height, lwidth = 0.8, labelsize = 10):
	fig2, ax = plt.subplots()
	fig2.subplots_adjust(left=.19, bottom=.17, right=.99, top=.97)

	Lp 			= 		len(P)
	Tp 			= 		np.arange(0, Lp/Fs, (1/Fs)).T
	Ppower 		= 		np.square(P)
	PpowerRev 	= 		Ppower[::-1]
	PEnergy		=		np.cumsum(PpowerRev)[::-1]
	PEdB        = 		10*np.log10(PEnergy)
	plt.plot(Tp, PEdB, ls='solid', color = 'k', linewidth=lwidth, label = 'Primary Path')
	
	if S is not None:
		Ls 			= 		len(S)
		Ts 			= 		np.arange(0, Ls/Fs, (1/Fs)).T
		Spower 		= 		np.square(S)
		SpowerRev 	= 		Spower[::-1]
		SEnergy		=		np.cumsum(SpowerRev)[::-1]
		SEdB        = 		10*np.log10(SEnergy)
		plt.plot(Ts, SEdB, ls='dashed', color = 'k', linewidth=lwidth, label = 'Secondary Path')
		
	plt.grid(True, which = 'both', linestyle=":", linewidth = 0.6)
	plt.minorticks_on()
	ax.minorticks_on()
	plt.xlabel('$Time(sec)$')
	plt.ylabel('$Energy(dB)$')
	plt.legend(loc='lower left',fontsize = 12)
	plt.show()

	# fig2.set_size_inches(width, height)
	# fig2.savefig('EnergyDecayCurve.pdf')
	
def SecondaryPathGraphs(e_iden, Sw, Shw, width = width, height = width/1.618):
	fig3 = plt.figure()
	fig3.subplots_adjust(left=.19, bottom=.17, right=.99, top=.97)

	plt.subplot(2,1,1)
	plt.plot(e_iden[0], label='Identification error')
	plt.ylabel('Amplitude')
	plt.xlabel('Discrete time k')
	plt.legend()

	plt.subplot(2,1,2)
	plt.stem(Sw, markerfmt='o',label='Coefficients of Sz') 
	#plt.stem(Shw[0, :], markerfmt='*',label='Coefficients of Shz')
	plt.stem(Shw, markerfmt='*',label='Coefficients of Shz')
	plt.ylabel('Amplitude');
	plt.xlabel('Numbering of filter tap');
	plt.legend()
	plt.show()

	# fig3.set_size_inches(width, height)
	# fig3.savefig('SecondaryPathDetails.pdf')


def ANCGraphs(ANCRed, e_cont, Yd, width = width, height = width/1.618):
	fig4 = plt.figure()
	fig4.subplots_adjust(left=.19, bottom=.17, right=.99, top=.97)

	plt.subplot(3,1,1)
	plt.plot(e_cont, label='Noise residue', linewidth=lwidth)
	plt.ylabel('Amplitude')
	plt.xlabel('Discrete time k')
	# plt.legend()

	plt.subplot(3,1,2)
	plt.plot(Yd,label='Noise signal', color='r', alpha=0.5, linewidth=lwidth)
	plt.plot(Yd-e_cont, color='b', ls='dashed', label='Control signal', linewidth=lwidth)
	plt.ylabel('Amplitude');
	plt.xlabel('Discrete time k');
	# plt.legend()
	# plt.show()

	plt.subplot(3,1,3)
	plt.plot(ANCRed,label='Noise signal', color='r', alpha=0.5, linewidth=lwidth)
	plt.ylabel('ANCRed');
	plt.xlabel('Discrete time k');
	plt.legend()
	plt.show()

	fig4.set_size_inches(width, height)
	fig4.savefig('ANCResults.pdf')



