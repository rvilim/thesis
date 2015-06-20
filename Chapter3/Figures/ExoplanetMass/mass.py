import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import matplotlib.patches as mpatches

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

planets=pd.read_csv('MassRadius_oec.csv')

planets['MASS']=planets['MASS']*317.828133
planets['R']=planets['R']*11.209

planets=planets.dropna(subset=['MASS'])

plt.figure(figsize=(12, 9))  
plt.xlim(.1, 100000)

# Remove the plot frame lines. They are unnecessary chartjunk.  
ax = plt.subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
  
# Ensure that the axis ticks only show up on the bottom and left of the plot.  
# Ticks on the right and top of the plot are generally unnecessary chartjunk.  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
  
ax.set_xscale('log')

# Make sure your axis ticks are large enough to be easily read.  
# You don't want your viewers squinting to read your plot.  
plt.xticks(fontsize=14)  
# yticks(range(5000, 30001, 5000), fontsize=14)
  
# Along the same vein, make sure your axis labels are large  
# enough to be easily read as well. Make them slightly larger  
# than your axis tick labels so they stand out.  
ax.set_xlabel(r'Mass $($M$_\oplus)$',fontsize=18)
ax.set_ylabel("Count", fontsize=18)  
  
# Plot the histogram. Note that all I'm passing here is a list of numbers.  
# matplotlib automatically counts and bins the frequencies for us.  
# "#3F5D7D" is the nice dark blue color.  
# Make sure the data is sorted into enough bins so you can see the distribution.  
plt.hist(planets['MASS'].values, color=tableau20[14], bins=np.logspace(0.1, 100, 1000))

plt.savefig('ExoplanetsMass.eps',  bbox_inches='tight')
plt.show()

