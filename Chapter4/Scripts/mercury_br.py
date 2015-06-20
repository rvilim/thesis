import matplotlib.pyplot as plt
import matplotlib.cm as colours
import pylab as m
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import matplotlib.ticker as ticker
from pylab import *

def getbr(lats,lons):
    
    ph=lons
    th=lats+np.pi/2
    print th
    
    costh=np.cos(th)
    legendrep10=costh
    l=1
    br=-(l+1)*((a/r)**(l+2))*g10*legendrep10
    
    legendrep20=.5*(3.0*(costh**2)-1.0)
    l=2
    br+=-(l+1)*((a/r)**(l+2))*g20*legendrep20
    
    return br
    
g10=195.0
g20=g10*.38
r=1.0
a=0.8

nlats = 73; nlons = 145; delta = 2.*np.pi/(nlons-1)

lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
lons = (delta*np.indices((nlats,nlons))[1,:,:])

cdict = {
'red'  :  ((0., 0.106, 0.106), (0.5, .92157, .94902), (1., .729, .729)),
'green':  ((0., 0.353, 0.353), (0.5, .92549, .94118), (1., .157, .157),),
'blue' :  ((0., 0.612, 0.612), (0.5, .92941, .94118), (1., .196, .196))
}

contourdict = {
'red'  :  ((0., 0.106, 0.106), (0.5, .106, .729), (1., .729, .729)),
'green':  ((0., 0.353, 0.353), (0.5, .353, .157), (1., .157, .157)),
'blue' :  ((0., 0.612, 0.612), (0.5, .612, .196), (1., .196, .196))
}

br=getbr(lats,lons)

rb_cmap = m.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
contour_cmap = m.matplotlib.colors.LinearSegmentedColormap('contour_colormap', contourdict, 1024)
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
#
map = Basemap(projection='moll',lat_0=0,lon_0=0,resolution='l')
x, y = map(lons*180./np.pi, lats*180./np.pi)

cs=map.contour(x,y,br,20,linewidths=.5,cmap=contour_cmap)#
cs.set_clim(-200, 200) 
q=0
for c in cs.collections:
    if(cs.levels[q]<0):
        c.set_linestyle('dashed')
  	
    if(cs.levels[q]==0):
        c.set_color((.533, .533, .533))
        c.set_linestyle('solid')
    q=q+1
    
#filled contours in colour       
cs=map.pcolor(x,y,br,cmap=rb_cmap)
cs.set_clim(-200, 200) 
colorbar()

m.savefig('Mercury_br.eps')