import pandas as pd
import matplotlib.pyplot as plt

#######################################################################################

width  			= 	3.5
height 			= 	width / 1.618
labelsize 		= 	10
legendfont 		= 	7
lwidth          =   0.8

plt.rc('pdf', fonttype = 42)
plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=labelsize)
plt.rc('ytick', labelsize=labelsize)
plt.rc('axes', labelsize=labelsize)

#########################################################################################

data 	= 	pd.read_excel(open('Results/Results__Zpos_0.82_UnClustered.xlsx','rb'), index=False)
print data.describe().iloc[:,-1]

fig, ax = plt.subplots()
fig.subplots_adjust(left=.2, bottom=.2, right=.97, top=.90)
plt.scatter(data['SSpectroFlat'], data['ANCRed'],c ='k', s = 2)
plt.xlabel('Spectral Flatness')
plt.ylabel('$ANC_{Red}$')
# plt.show()

fig.set_size_inches(width, height)
fig.savefig('SpectralFlatSimResult.png', dpi = 600)
plt.close()