import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import matplotlib.patches as mpatches

ssradius=np.array([2440, 6052, 6378, 3397, 71492, 60268, 25559, 24766]) / 6378.0

ssmass=np.array([3.30E23, 4.87E24, 5.97E24, 6.42E23, 1.90E27, 5.68E26, 8.68E25, 1.02E26]) / 5.97E24

def mr(M,m1,r1,k1,k2,k3):
    return r1*np.power(10.0,k1+np.log10(M/m1)/3.0-k2*np.power(M/m1,k3))
    
def massradiussolid(M,m1,r1,k1,k2,k3, k1m=0,k2m=0,k3m=0):
    # This just reproduces the relations in seager 2007
    
    if(k1m!=0 or k2m!=0 or k3m!=0):
        radius=[mr(mass,m1,r1,k1,k2,k3) if mass/m1<4 else mr(mass,m1,r1,k1m,k2m,k3m) for mass in M ]
    else:
        radius=mr(M,m1,r1,k1,k2,k3)
    return radius

def mrhydrogen(R,M,Zz,Aa):
    # This solves the relation in Zapolsky and Salpeter (1969)
    
    earthmasscm=5.97219E27
    M=M*earthmasscm
    
    P0=lambda Z: 9.52E13*np.power(Z,10.0/3)
    R0=lambda ZA: 9.73E9*(ZA[0]/ZA[1])*np.power(ZA[0],-1.0/3.0)
    M0=lambda ZA: 3.58E30*ZA[0]*np.power(ZA[0]/ZA[1],2)
    phi = lambda Z: np.power(3,1.0/3.0)/20.0+(1.0/8.0)*np.power(.75*np.power(np.pi*Z,-2.0),1.0/3.0)
    beta = lambda Z: 3.562+5.634/np.sqrt(Z)
    alpha = lambda Z: np.power(beta(Z),5.0/3.0)/.4242
    
    f=np.power(M/M0([Zz,Aa]),1.0/3.0)*(R/R0([Zz,Aa]))
    f=f-(alpha(Zz)/np.power(beta(Zz),5.0/3.0))*np.power(1-np.power(np.power(R,3.0)*M0([Zz,Aa])/(np.power(R0([Zz,Aa]),3)*M),1.0/3.0)*phi(Zz),5.0)
    
    return f
    
def massradiushydrogen(M):
    Z=1.0
    A=1.9
    
    earthradcm=637810000.0
    
    return [ opt.brentq(mrhydrogen, 100, 2E10, maxiter=10000, args=(mass,Z,A))/earthradcm for mass in M]

# These are the "Tableau 20" colors as RGB.  
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  
  
# You typically want your plot to be ~1.33x wider than tall. This plot is a rare  
# exception because of the number of lines being plotted on it.  
# Common sizes: (10, 7.5) and (12, 9)  
plt.figure(figsize=(12, 9))
  
# Remove the plot frame lines. They are unnecessary chartjunk.  
ax = plt.subplot(111)  

# Limit the range of the plot to only where the data is.  
# Avoid unnecessary whitespace.  
plt.ylim(0.1, 30)
plt.xlim(.01, 10000)
  
# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
# plt.yticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=14)
# plt.xticks(fontsize=14)

# planets=pd.read_csv('MassRadius.csv')
planets=pd.read_csv('MassRadius_oec.csv')

planets['MASS']=planets['MASS']*317.828133
planets['R']=planets['R']*11.209
#
massrange=np.linspace(.01,10000,10000)
#
planets=planets.dropna()

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)  
ax.set_xscale('log')
ax.set_yscale('log')

# Ensure that the axis ticks only show up on the bottom and left of the plot.  
# Ticks on the right and top of the plot are generally unnecessary chartjunk.  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  

plt.setp(ax.get_xticklabels(), fontsize=14)
plt.setp(ax.get_yticklabels(), fontsize=14)

ax.set_xlabel(r'Mass $($M$_\oplus)$',fontsize=18)
ax.set_ylabel(r'Radius $($R$_\oplus)$',fontsize=18)

plt.scatter(planets['MASS'].values,planets['R'].values,color=tableau20[14], edgecolor='black')

plt.plot(massrange,massradiussolid(massrange,5.80, 2.52, -.20945, .0804, .394, -.209490, .0804, .394),color=tableau20[4])
plt.plot(massrange,massradiussolid(massrange,6.41, 3.19, -.20945, .0804, .394),color=tableau20[0])
plt.plot(massrange,massradiussolid(massrange,8.16, 4.73, -.20945, .0804, .394),color=tableau20[1])
plt.plot(massrange,massradiushydrogen(massrange),color=tableau20[6])
plt.scatter(ssmass, ssradius, s=ssradius*0.0+100, alpha=.7,color=tableau20[2], edgecolor='black')

Iron = mpatches.Patch(color=tableau20[4], label='Fe')
Earth = mpatches.Patch(color=tableau20[0], label='Earth-like')
Water = mpatches.Patch(color=tableau20[1], label=r'H$_{2}$O')
Hydrogen = mpatches.Patch(color=tableau20[6], label='H')
SolarSystem = mpatches.Patch(color=tableau20[2], label='Solar System',alpha=.7)
Exoplanets = mpatches.Patch(color=tableau20[14], label='Exoplanets')

plt.legend(handles=[Iron, Earth, Water, Hydrogen, SolarSystem, Exoplanets],loc=4)

plt.savefig('Exoplanets.eps', bbox_inches='tight')
# red_patch = mpatches.Patch(color='red', label='The red data')
# plt.legend(handles=[red_patch])

plt.show()

print len(planets)
