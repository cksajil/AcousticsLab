import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

width  = 3.5
height = width / 1.618
labelsize 	= 10
legendfont 	= 9

plt.rc('font', family = 'serif')
plt.rc('text', usetex = True)
plt.rc('xtick', labelsize=labelsize)
plt.rc('ytick', labelsize=labelsize)
plt.rc('axes', labelsize=labelsize)

TransSeparation  =    0.05
xpos             =    np.around(np.arange(0.1, 2.9, TransSeparation),2)
ypos             =    np.around(np.arange(0.1, 2.14, TransSeparation),2)


data 	=	pd.read_excel(open('Results/Results__Zpos_0.82_UnClustered.xlsx','rb'), index=False)
column 	= 	'ANCRed'
y 		= 	data[column]
W 		= 	41
N 		= 	y.shape[0]
H 		= 	N/W
I 		= 	y.values.reshape((H, W)).T


fig, ax = plt.subplots()
fig.subplots_adjust(left=0.07, bottom=.09, right=1.02, top=0.99)
plt.imshow(I, origin='upper', cmap = 'viridis')

Sx, Sy 			= 	1.4, 2.0
Rx, Ry 			= 	1.4, 1.0
Ax, Ay			= 	2.85,0.1

Sxi, = np.where( xpos==Sx )
Syi, = np.where( ypos==Sy )
Rxi, = np.where( xpos==Rx )
Ryi, = np.where( ypos==Ry )
# Axi, = np.where( xpos==Ax )
# Ayi, = np.where( ypos==Ay )



Slabel 	= 	'Noise Source ('+str(Sx)+', '+str(Sy)+')'
Rlabel 	= 	'Microphone ('+str(Rx)+', '+str(Ry)+')'
# Alabel 	= 	'Best position ('+str(Ax)+', '+str(Ay)+')'

plt.plot(Sxi,Syi,'+', color ='k', label=Slabel)
plt.plot(Rxi,Ryi,'o', markerfacecolor = 'None', markeredgecolor='b', label=Rlabel)
# plt.plot(Axi,Ayi,'*', markerfacecolor = 'None', markeredgecolor='y', label=Alabel)
plt.legend(loc='upper right', fontsize = legendfont, framealpha=0.4)

plt.xlabel('X position')
plt.ylabel('Y position')
plt.colorbar()

frame1 	= 	plt.gca()
frame1.axes.xaxis.set_ticklabels([])
frame1.axes.yaxis.set_ticklabels([])
ax.set_xticks([])
ax.set_yticks([])


fig.set_size_inches(width, height)
plt.savefig('Colorplane.png', dpi = 600)
plt.close()

