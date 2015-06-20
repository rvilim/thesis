import plotfunctions
import gausscoefficients
import custom
import sys

# This program will output a plot of br at a given radius from the gauss coefficients. 
# The gauss coeffiients are set in .py files named after the planet, these are combined
# into a big dictionary in gausscoefficients.py 

# To use this specify nlats and nlons (the number of points
# in the theta and phi) and the planet below. The planet values can be

# Mercury, Earth, Jupiter, Saturn, Uranus, Neptune

# you can also specify "All" as a planet and it will plot all the planets it has in the database

# But you can add more. Also, if a gauss coefficient is not specified it is taken to be zero

# In the files that specify the gauss coefficients we have glm and hlm, but also Glm and Hlm
# these correspond to the gauss coefficients of the external field. Again, if you leave them
# blank they are taken to be zero.

# Finally there are two optional arguments to plotb, r and units. r is the radius at which you
# want the magnetic field and units are the units of r. By default I assume you want the magnetic
# field at the surface, if you leave these blank that's what you'll get. Remember that this expansion
# is only valid above the dynamo region so set r accordingly.

# units can be either "Rp" or "Km", these just specify the units that r is in, whether it is in 
# planetary radii or kilometers. If you leave it blank I assume it is in planetary radii.

nlats = 240
nlons = 480
planet="Custom"

if((planet=="Custom") or (planet=="All" and sys.argv[1]!="")):
    customcoeffs=custom.custom(sys.argv[1])
    # gausscoefficients.gcoeff.update(customcoeffs)
    
if(planet=="All"):
    # Get all the planets in the dictionary by making a list comprehension of the first element
    # in the tuple of keys and converting it to a set (a sets elements must be unique, so it)
    # strips out the duplicates.
    
    planets=set([x[0] for x in gausscoefficients.gcoeff.keys()])
    
    for planet in planets:
        print "Plotting "+planet+"..."
        plotfunctions.plotb(nlats,nlons,planet)
else:
    # If we specified an actual planets
    plotfunctions.plotb(nlats,nlons,planet,r=1)    