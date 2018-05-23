import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

width  = 3.5
#height = 2.5
height = width / 1.618
labelsize 	= 10
legendfont 	= 9

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=labelsize)
plt.rc('ytick', labelsize=labelsize)
plt.rc('axes', labelsize=labelsize)

TransSeparation     	=       0.11 
xpos 					= 		np.arange(0.1, 6, TransSeparation)
ypos 					= 		np.arange(0.1, 4, TransSeparation)

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

for i in range(0,25):

	data 	= 	pd.read_csv('Results/Results_Zpos_1_53_Cluster_3.csv')[i*1944:(i+1)*1944]
	column 	= 	'Attenuation'
	y 		= 	data[column]

	GoodCutoffH 	= 	np.mean(y)
	GoodPos 		= 	(y>GoodCutoffH)

	W 				= 	36
	N 				= 	y.shape[0]
	H 				= 	N/W
	Ig 				= 	GoodPos.values.reshape((H, W)).T


	xvalues = data['Ax']
	yvalues = data['Ay']
	xmax 	= np.amax(xvalues)
	ymax 	= np.amax(yvalues)

	fig, ax = plt.subplots()
	fig.subplots_adjust(left=0.07, bottom=.09, right=0.99, top=0.99)

	plt.imshow(Ig, origin='upper', cmap='Greys')

	Sx, Sy = data.iloc[1,1:3].values
	Rx, Ry = data.iloc[1,4:6].values

	Sx = find_nearest(xpos,Sx)
	Sy = find_nearest(ypos,Sy)
	Rx = find_nearest(xpos,Rx)
	Ry = find_nearest(ypos,Ry)

	Sxi, = np.where( xpos==Sx )
	Syi, = np.where( ypos==Sy )
	Rxi, = np.where( xpos==Rx )
	Ryi, = np.where( ypos==Ry )

	Slabel = 'Noise Source('+str(Sx)+', '+str(Sy)+')'
	Rlabel = 'Microphone('+str(Rx)+', '+str(Ry)+')'

	plt.plot(Sxi,Syi,'+', color ='r', label=Slabel)
	plt.plot(Rxi,Ryi,'o', markerfacecolor = 'None', markeredgecolor='b', label=Rlabel)
	plt.plot([],[], marker='s', markersize=3, linewidth=0, color = 'k', label='$A_{dB}>=C$')
	plt.legend(loc='lower left', fontsize = legendfont, framealpha=0.4)

	plt.xlabel('x position')
	plt.ylabel('y position')

	frame1 = plt.gca()
	frame1.axes.xaxis.set_ticklabels([])
	frame1.axes.yaxis.set_ticklabels([])
	ax.set_xticks([])
	ax.set_yticks([])

	fig.set_size_inches(width, height)
	plt.savefig('ColorplaneSigma_'+str(i)+'.pdf', dpi = 600)
	plt.close()
