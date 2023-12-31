import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# import healpy as hp # doesn't work on windows
# from astropy.io import ascii

cmap2d = mpl.colormaps['binary']

fullCirc = 360 # sets units

"""
To DO
live planets?
label brightest of each constellation?
"""

# data = ascii.read('../bsc5.dat')  
# data = pd.read_table('../bsc5.dat') # neither works well due to missing values

#reading
with open('../bsc5.dat','rt') as f:
    lines = f.readlines()

#cleaning
toPop = []
for i in range(len(lines)):
    if lines[i][75] == ' ':
        toPop.append(i)
        
toPop.reverse() # to stop line numbers changing
for i in toPop:
    lines.pop(i)

data = np.zeros((len(lines), 3))

for i in range(len(lines)):
    data[i,0] = (  float(lines[i][75:77])
                 + float(lines[i][77:79])/60
                 + float(lines[i][79:83])/(60*60)
                 )*fullCirc/24
    
    data[i,1] = (  float(lines[i][84:86])
                 + float(lines[i][86:88])/60
                 + float(lines[i][88:90])/(60*60)
                 )*(fullCirc/360)*(1 if lines[i][83]=='+' else -1)
    
    data[i,2] = float(lines[i][102:107])
    
data[:,0] -= fullCirc/2 #arbitrary adjust to put plough in middle
    
data[:,0] = data[:,0]%(fullCirc)
data[data[:,0]>fullCirc/2, 0] -= fullCirc

cutoff=3.5
magMask = data[:,2]<cutoff

# full sky rectilinear
fig,ax = plt.subplots()
ax.scatter(-data[magMask,0], data[magMask,1], s=2.0*(cutoff-data[magMask,2]), c='k')
fig.savefig('../RL.pdf')

#North hemisphere
rlim = fullCirc/6
NMask = data[:,1]>fullCirc/4-rlim
theta = -data[magMask&NMask,0]*2*np.pi/fullCirc
r = fullCirc/4 - data[magMask&NMask,1]
fig,ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(theta, r, s=2.0*(cutoff-data[magMask&NMask,2]), c='k')
ax.set_rticks([])
ax.set_rlim([0,rlim])
fig.savefig('../North.pdf')


#North hemisphere
SMask = data[:,1]<-(fullCirc/4-rlim)
theta = data[magMask&SMask,0]*2*np.pi/fullCirc
r = fullCirc/4 + data[magMask&SMask,1]
fig,ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.scatter(theta, r, s=2.0*(cutoff-data[magMask&SMask,2]), c='k')
ax.set_rticks([])
ax.set_rlim([0,rlim])
fig.savefig('../South.pdf')


# hp.newvisufunc.projview( hp dpesn't work on windows
#     np.zeros(hp.order2npix(4)), graticule=True, graticule_labels=True,
#     projection_type="mollweide", cmap=cmap2d, cbar=False,
#     # custom_xtick_labels=['300°','240°','180°','120°','60°'], - Double check directions!
#     xlabel=r"ra",
#     ylabel=r"dec",
#     # title='ISO Radiant'
# )
# fig = plt.gcf()
# ax = fig.get_axes()[0]
# ax.scatter(-data[mask,0],data[mask,1], s=1.0*(cutoff-data[mask,2]), c='k')
