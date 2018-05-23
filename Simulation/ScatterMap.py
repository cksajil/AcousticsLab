import numpy as np
import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec

result	=	pd.read_excel(open('Results/Results__Zpos_0.82_UnClustered.xlsx','rb'), index=False)
print result.describe().iloc[:,-1]


width  			= 		3.5
height 			= 		width / 1.618
labelsize 		= 		10
legendfont 		= 		6
data 			= 		result
column 			= 		'ANCRed'
y 				= 		data[column]
x 				= 		np.sqrt((1.4 -data.iloc[:,6])**2+(2.0-data.iloc[:,7])**2)
mu 				= 		np.mean(y)
stdlow  		= 		mu-1.96*np.std(y)
stdhigh 		=		mu+1.96*np.std(y)

plt.rc('pdf', fonttype = 42)
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=labelsize)
plt.rc('ytick', labelsize=labelsize)
plt.rc('axes', labelsize=labelsize)


fig 		= plt.figure()
fig.subplots_adjust(left=0.2, bottom=.20, right=.99, top=.97)

gspec 		= 		gridspec.GridSpec(1, 5)
hist 		= 		plt.subplot(gspec[0,4])
scat 		= 		plt.subplot(gspec[0,0:4])

scat.scatter(x, y, alpha=0.8, color='k', s=1, marker='o', linewidth=0.1, label='$ANC_{Red}$')
# scat.axhline(y = mu, alpha=0.8, linestyle = '-', color='b', linewidth=1, label='$\mu_{ANC_{Red}}$')
#plt.plot(x, stdlow, color='r', linewidth='0.6', label='$\mu_{A_{dB}}-2*\sigma_{A_{dB}}$')
# scat.axhline(y = stdhigh, alpha=0.8, linestyle = '--', color='g', linewidth=1, label='$\mu_{ANC_{Red}}+1.96*\sigma_{ANC_{Red}}$')
#scat.yaxis.tick_right()
#scat.yaxis.set_label_position("right")

plt.xlabel('Anti-noise source to microphone distance')
plt.ylabel('$ANC_{Red}$')
#plt.xlim((0,8.5))
#plt.ylim((0,15))
#plt.grid(True, which='both', linestyle='--', linewidth='0.3')
# plt.legend(loc='upper left', fontsize = legendfont, framealpha=0.7, borderpad=0.15, labelspacing = 0.1, handlelength=1, handletextpad= 0.1, borderaxespad=0.1,columnspacing=0.1)
# plt.legend(loc='upper left', fontsize = legendfont)

s = hist.hist(y, bins = 40, orientation='horizontal', normed = True)
#hist.invert_xaxis()
hist.axis('off')


fig.set_size_inches(width, height)
plt.savefig('Attenuation.png', dpi = 600)
