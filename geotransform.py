from math import *

rad = 57.2957795

def deg2rad(x):
    return (x/rad)

def deglon_metres(x):
    d2r=deg2rad(x)
    return((111415.13 * cos(d2r))- (94.55 * cos(3.0*d2r)) + (0.12 * cos(5.0*d2r)))

def deglat_metres(x):
    d2r=deg2rad(x)
    return(111132.09 - (566.05 * cos(2.0*d2r))+ (1.20 * cos(4.0*d2r)) - (0.002 * cos(6.0*d2r)))

def translatexy2ll(localx,localy,originx=0,originy=0,rotateangle=0,xoffset=0,yoffset=0): 
    xx,yy,r,ct,st,angle=0,0,0,0,0,0
    angle = deg2rad(rotateangle)
    xpos = localx;  
    ypos = localy;
    xx = xpos - xoffset;
    yy = ypos - yoffset;
    r = sqrt(xx*xx + yy*yy);
    if(r):
      ct = xx/r
      st = yy/r
      xx = r * ( (ct * cos(angle))+ (st * sin(angle)) )
      yy = r * ( (st * cos(angle))- (ct * sin(angle)) )
    plon = originy + xx/deglon_metres(originx)
    plat = originx + yy/deglat_metres(originx)
    return(plat,plon)

def translatell2xy(locallat,locallon,originlon=0,originlat=0,rotateangle=0,xoffset=0,yoffset=0): 
    xx,yy,r,ct,st,angle=0,0,0,0,0,0
    angle = deg2rad(rotateangle)
    xx = (locallon - originlon)*deglon_metres(originlat)
    yy = (locallat - originlat)*deglat_metres(originlat)
    r = sqrt(xx*xx + yy*yy);
    if(r):
      ct = xx/r
      st = yy/r
      xx = r * ( (ct * cos(angle)) + (st * sin(angle)) )
      yy = r * ( (st * cos(angle)) - (ct * sin(angle)) )
    xpos = xx + xoffset
    ypos = yy + yoffset
    return(xpos,ypos)   

# lat = -35.363262
# lon = 149.165237
# a = []
# b = []

# a = translatell2xy(lat,lon)
# b = translatexy2ll(a[0],a[1])
# print (a[0])
# print (a[1])
# print (b[0])
# print (b[1])     