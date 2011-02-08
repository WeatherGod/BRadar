import os.path			# for os.path.dirname(), os.path.abspath(), os.path.sep
import numpy as np


#################################
#    Basemap-related portion    #
#-------------------------------#
# Default Map display options
mapLayers = [['states', {'linewidth':1.5, 'color':'k', 'zorder':0}],
             ['counties', {'linewidth':0.5, 'color':'k', 'zorder':0}],
             ['roads', {'linewidth':0.75, 'color':'r', 'zorder':0}],
             ['rivers', {'linewidth':0.5, 'color':'b', 'zorder':0}]]



def PlotMapLayers(map, layerOptions, axis=None):

    for layer in layerOptions :
        if layer[0] == 'states' :
            map.drawstates(ax=axis, **layer[1])
        elif layer[0] == 'counties' :
            map.readshapefile(os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), 'shapefiles', 'countyp020']),
                              name='counties', ax=axis, **layer[1])
        elif layer[0] == 'rivers' :
            map.drawrivers(ax=axis, **layer[1])
        elif layer[0] == 'roads' :
            map.readshapefile(os.sep.join([os.path.dirname(os.path.abspath(__file__)), 'shapefiles', 'road_l']),
                              name='road', ax=axis, **layer[1])
        elif layer[0] == 'countries':
            map.drawcountries(ax=axis, **layer[1])
        else :
            raise TypeError('Unknown map_layer type: ' + layer[0])
#------------------------------#
################################


################################
#  General geographic portion  #
#------------------------------#
def sph2latlon(locLat, locLon, azis, gates, elevAngle) :
   """
   azis and gates are parallel vectors (or matrix) of azimuth angles (0 deg is
   north) and Range Gate distance (meters).  locLat and locLon are the
   latitude and longitude of the station in degrees.  elevAngle is the
   elevation angle in degrees.

   RETURNS: latout and lonout are vectors (or matricies)
   parallel to the spherical coordinates specified.
   Assumes that calculation applies to Earth.

   (Double-check this statement)
   Also, does not account for curvature of planet when determining the ground
   distance covered by the radial.
   """
   groundDist = gates * np.cos(np.radians(elevAngle))
   latout, lonout = LatLonFrom(locLat, locLon, groundDist, azis)
   return (latout, lonout)


def GreatCircleDist(fromLons, fromLats, toLons, toLats, radius=6367470.0) :
    """
    Input latitudes and logitudes are in DEGREES.
    Output distance is in the same units as the input radius.

    By default, input radius is the earth's radius in Meters.
    """
    fromLons = np.radians(fromLons)
    fromLats = np.radians(fromLats)
    toLons = np.radians(toLons)
    toLats = np.radians(toLats)

    return(radius * 2.0 * np.arcsin(np.sqrt(np.sin((toLats - fromLats)/2.0) ** 2
                          + np.cos(fromLats) * np.cos(toLats)
                        * np.sin((toLons - fromLons)/2.0)**2)))

def Bearing(fromLons, fromLats, toLons, toLats) :
    """
    Input longitudes and latitudes are in DEGREES.
    Output bearing is in RADIANS North.

    RETURNS Bearing
    """
    fromLons = np.radians(fromLons)
    fromLats = np.radians(fromLats)
    toLons = np.radians(toLons)
    toLats = np.radians(toLats)

    return np.arctan2( np.sin(toLons - fromLons) * np.cos(toLats),
                       (np.cos(fromLats) * np.sin(toLats) -
                        np.sin(fromLats) * np.cos(toLats) *
                        np.cos(toLons - fromLons)) )

def LatLonFrom(fromLat, fromLon, dist, azi, radius=6367470.0) :
    """
    Input and output longitudes and latitudes are in DEGREES.
    
    RETURNS (toLat, toLon)
    """
    fromLat = np.radians(fromLat)
    fromLon = np.radians(fromLon)
    azi = np.radians(azi)

    radianDist = dist/radius

    toLat = np.arcsin(np.sin(fromLat)*np.cos(radianDist)
               + np.cos(fromLat)*np.sin(radianDist)*np.cos(azi))
    dlon = np.arctan2(-np.sin(azi)*np.sin(radianDist)*np.cos(fromLat),
             np.cos(radianDist)-np.sin(fromLat)*np.sin(fromLat))
    toLon = zero22pi(fromLon - dlon + np.pi) - np.pi

    return (np.degrees(toLat), np.degrees(toLon))

def npi2pi(inAngle) :
    return (np.pi * ((np.abs(inAngle)/np.pi) -
                    2.0*np.ceil(((np.abs(inAngle)/np.pi)-1.0)/2.0)) *
            np.sign(inAngle))

def zero22pi(inAngle) :
    outAngle = npi2pi(inAngle)
    return outAngle + np.where(outAngle < 0.0, 2.0 * np.pi, 0.0)

def makerefmat(crnrlon, crnrlat, dx, dy) :
    return np.dot(np.array([[0.0, dx, crnrlon],
                  [dy, 0.0, crnrlat]]),
             np.array([[0.0, 1.0, -1.0],
                  [1.0, 0.0, -1.0],
                  [0.0, 0.0, 1.0]])).conj().T


def map2pix(refMat, X, Y) :
    (col, row) = np.linalg.solve(refMat[0:2, :].T,
                     np.array([X.flat - refMat[2, 0], Y.flat - refMat[2, 1]]))
    row.shape = Y.shape
    col.shape = X.shape
    return (row, col)

def latlon2pix(refMat, lat, lon) :
    # The following is a bit convoluded, but it is to get rid
    # of any possible issues with longitudinal abiguity
    [row1, col1] = map2pix(refMat, lon, lat)
    [row2, col2] = map2pix(refMat, lon + 360.0, lat)

    [rowsLow, rowsUp] = find_limits(row1, row2)
    [colsLow, colsUp] = find_limits(col1, col2)

    cycleCnt = np.maximum(rowsLow, colsLow)
    indicate = np.minimum(rowsUp, colsUp)
    cycleCnt[np.isinf(cycleCnt)] = indicate[np.isinf(cycleCnt)]
    cycleCnt[np.isinf(cycleCnt)] = 0

    [row, col] = map2pix(refMat, lon + 360.0 * cycleCnt, lat)
    # need to correct for 0-base indexing
    return (row - 1, col - 1)

def find_limits(index1, index2) :
    diff = index2 - index1
    Z = (0.5 - index1) / diff
    lowerLims = np.where(diff > 0.0, np.ceil(Z), -np.inf)
    upperLims = np.where(diff < 0.0, np.floor(Z), np.inf)
    return (lowerLims, upperLims)
#------------------------------#
################################




