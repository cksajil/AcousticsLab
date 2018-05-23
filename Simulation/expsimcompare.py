import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

width  		= 	6
height 		= 	width / 1.618
lwidth 		= 	0.8
labelsize 	= 	12

fig = plt.figure()
fig.subplots_adjust(left=.19, bottom=.17, right=.99, top=.97)

plt.rc('font', family='serif')
plt.rc('text', usetex=True)
plt.rc('xtick', labelsize = labelsize)
plt.rc('ytick', labelsize = labelsize)
plt.rc('axes', labelsize  = labelsize)


exp  =   pd.read_excel(open('Compare.xlsx','rb'), index=False)['Exp']
sim  =   pd.read_excel(open('Compare.xlsx','rb'), index=False)['Sim']

exp  = 	 (exp-np.min(exp))/(np.max(exp)-np.min(exp))
sim  = 	 (sim-np.min(sim))/(np.max(sim)-np.min(sim))

plt.scatter(sim, exp)

plt.ylabel('Experiment');
plt.xlabel('Simulation');
plt.show()

fig.set_size_inches(width, height)
fig.savefig('ExpSimScatter.pdf')
