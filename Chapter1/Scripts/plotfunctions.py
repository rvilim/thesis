import matplotlib.pyplot as plt
import matplotlib.cm as colours
import pylab as m
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import matplotlib.ticker as ticker
from pylab import *
from scipy.special import lpmv
from scipy.misc import factorial
import gausscoefficients
import sys

def getbr(lats,lons,planet, a, r, Lmax):
    ph=lons-np.pi
    th=lats-np.pi/2
    
    costh=np.cos(th)

    br=np.zeros_like(lats)
    
    cosmph=[]
    sinmph=[]
    
    for m in xrange(0,Lmax+1):
        cosmph.append(np.cos(m*ph))
        sinmph.append(np.sin(m*ph))
    
    
    for L in xrange(1,Lmax+1):

        for m in xrange(L+1):
            print "L=",L," m=",m
            glm=gausscoefficients.gcoeff.get((planet,"g",L,m),0.0)
            hlm=gausscoefficients.gcoeff.get((planet,"h",L,m),0.0)
            
            Glm=gausscoefficients.gcoeff.get((planet,"G",L,m),0.0)
            Hlm=gausscoefficients.gcoeff.get((planet,"H",L,m),0.0)
            
            if(m!=0):
                schmidt=np.sqrt(2.0*factorial(L-m)/factorial(L+m))
            else:
                schmidt=1.0

            legendrep=lpmv(m,L,costh[:,1])
            
            if(L==50 and m==49):
                print costh[:,1]
                print legendrep
            # print costh[:,1]
            # print "ph=",ph[1,2]
            # print "ph=",ph[1,2],"m=",m,"cosmph=",cosmph[m][1,2]
            for i in range(0,np.shape(ph[1,:])[0]):
                # print np.shape(ph[1,:])
                br[:,i]+=(L+1.0)*(((a/r)**(L+2.0))*(glm*cosmph[m][:,i]+hlm*sinmph[m][:,i])+((r/a)**(L))*(Glm*cosmph[m][:,i]+Hlm*sinmph[m][:,i]))*schmidt*legendrep
                # print cosmph[m][:,i]

    return br
    
def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    if(x==0):
        return r'${}$'.format(0)
        
    return r'${} \times 10^{{{}}}$'.format(a, b)

def plotb(nlats,nlons,planet,r=None, units="Rp"):
    
    # This is a list comprehension which goes through all the keys in my gcoeff dictionary, picks the L's 
    # for the planet we want, then makes sure that we are selecting g and h (as opposed to a) adds these all
    # to a list, then finds the maximum of these L's
    
    Lmax=max([x[2] for x in gausscoefficients.gcoeff.keys() if ((x[0]==planet) and(x[1]=="g" or x[1]=="h"))])
    
    Lmax=50
    # If we've specified our units to be in planetary radii, then a=1, otherwise it is the value of planetary
    # radius that got specified in the dictionary
    if(units=="Rp"):
        a=1.0;
    elif(units=="km"):
        a=gausscoefficients.gcoeff[(planet,"a")]
    else:
        sys.exit("Unknown unit specified")

    #If they haven't explicitly specified an r assume we are at the planetary surface (a)
    if r is None:
        r=a
    
    delta = 2.*np.pi/(nlons-1)

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

    br=getbr(lats,lons,planet, a, r, Lmax)

    rb_cmap = m.matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
    contour_cmap = m.matplotlib.colors.LinearSegmentedColormap('contour_colormap', contourdict, 1024)
    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

    nearestlat=np.min(np.min(lats))
    nearestlon=np.min(np.min(lons))

    map = Basemap(projection='hammer',lat_0=0,lon_0=0,resolution='l')

    x, y = map(lons*180./np.pi-180.0, lats*180./np.pi)

    cs=map.contour(x,y,br,20,linewidths=.5,cmap=contour_cmap)#

    limit=np.amax(np.amax(np.fabs(br)))
    cs.set_clim(-limit, limit)
    q=0
    for c in cs.collections:
        if(cs.levels[q]<0):
            c.set_linestyle('solid')

        if(cs.levels[q]==0):
            c.set_color((.533, .533, .533))
            c.set_linestyle('solid')
        q=q+1

    #filled contours in colour
    cs=map.pcolor(x,y,br,cmap=rb_cmap,rasterized=True)
    cs.set_clim(-limit, limit)
    cb=colorbar(shrink=.5, aspect=10,format=ticker.FuncFormatter(fmt))
    cb.ax.tick_params(labelsize=15)
    cb.solids.set_rasterized(True)  
    tick_locator = ticker.MaxNLocator(nbins=6)
    cb.locator = tick_locator
    cb.update_ticks()
    cb.set_label(r'$nT$',rotation=0,fontsize=20,y=0.56)
    m.savefig(planet+'.pdf',dpi=150) 
    clf()