import os.path			# for os.path.dirname(), os.path.abspath(), os.path.sep
import numpy as np


#################################
#    Basemap-related portion    #
#-------------------------------#
# Default Map display options
mapLayers = [('states', {'linewidth':1.5, 'color':'k', 'zorder':0}),
             ('counties', {'linewidth':0.5, 'color':'k', 'zorder':0}),
             ('roads', {'linewidth':0.75, 'color':'r', 'zorder':0}),
             ('rivers', {'linewidth':0.5, 'color':'b', 'zorder':0})]

def PlotMapLayers(bmap, layerOptions=None, axis=None, **kwargs) :
    """
    Easily plot various map elements.

    *bmap*          Basemap instance
    *layerOptions*  list of tuples containing a shortcut name and
                    a dictionary of style properties.
                    Names can be 'states', 'counties', 'rivers',
                                 'roads', and 'countries'.
                    If none is given, `mapLayers` is used.
    *axis*          Matplotlib axes object
    *kwargs*        Any keywords you wish to use to override or augment
                    the keywords used in *layerOptions*.
    """
    if layerOptions is None :
        layerOptions = mapLayers

    # TODO: Learn to use pkg_resources
    module_path = os.path.dirname(os.path.abspath(__file__))

    for layer in layerOptions :
        style = layer[1].copy()
        style.update(kwargs)
        if layer[0] == 'states' :
            bmap.drawstates(ax=axis, **style)
        elif layer[0] == 'counties' :
            bmap.readshapefile(os.path.join(module_path,
                                            'shapefiles', 'countyp020'),
                               name='counties', ax=axis, **style)
        elif layer[0] == 'rivers' :
            bmap.drawrivers(ax=axis, **style)
        elif layer[0] == 'roads' :
            bmap.readshapefile(os.path.join(module_path,
                                            'shapefiles', 'road_l'),
                               name='road', ax=axis, **style)
        elif layer[0] == 'countries':
            bmap.drawcountries(ax=axis, **style)
        else :
            raise ValueError('Unknown map_layer type: ' + layer[0])
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
    .. note ::
        The default value here has very little basis in accepted literature.
        When originally writing this function in C++, I merely took the
        straight average between the equatorial radius and the polar radius.
        A more valid value might be Q_r = 6372797.0 (equivalent great-circle
        radius of an Earth ellipsoid). However, I fear that changing this now
        might impact existing programs. Further investigations shall be done.
    """
    fromLons = np.radians(fromLons)
    fromLats = np.radians(fromLats)
    toLons = np.radians(toLons)
    toLats = np.radians(toLats)

    # Haversine formula
    return(radius * 2.0 * np.arcsin(np.sqrt(np.sin((toLats - fromLats)/2.0) ** 2
                          + np.cos(fromLats) * np.cos(toLats)
                        * np.sin((toLons - fromLons)/2.0)**2)))

def GreatCircleDist_Alt(fromLons, fromLats, toLons, toLats, radius=6367470.0) :
    fromLons = np.radians(fromLons)
    fromLats = np.radians(fromLats)
    toLons = np.radians(toLons)
    toLats = np.radians(toLats)

    # Vincenty formula
    c_toLats = np.cos(toLats)
    c_fromLats = np.cos(fromLats)
    s_toLats = np.sin(toLats)
    s_fromLats = np.sin(fromLats)
    deltaLons = toLons - fromLons

    return radius * np.arctan2(np.sqrt((c_toLats * np.sin(deltaLons)) ** 2 +
                                       (c_fromLats * s_toLats -
                                        s_fromLats * c_toLats *
                                        np.cos(deltaLons)) ** 2),
                               (s_fromLats * s_toLats +
                                c_fromLats * c_toLats * np.cos(deltaLons)))

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

def LatLonFrom_Alt(fromLat, fromLon, dist, azi, radius=6367470.0) :
    """
    Input and output longitudes and latitudes are in DEGREES.
    
    RETURNS (toLat, toLon)

    .. note ::
        The default value here has very little basis in accepted literature.
        When originally writing this function in C++, I merely took the
        straight average between the equatorial radius and the polar radius.
        A more valid value might be Q_r = 6372797.0 (equivalent great-circle
        radius of an Earth ellipsoid). However, I fear that changing this now
        might impact existing programs. Further investigations shall be done.
    """
    fromLat = np.radians(fromLat)
    fromLon = np.radians(fromLon)
    azi = np.radians(azi)

    radianDist = dist/radius

    toLat = np.arcsin(np.sin(fromLat) * np.cos(radianDist) +
                      np.cos(fromLat) * np.sin(radianDist) * np.cos(azi))
    dlon = np.arctan2(-np.sin(azi) * np.sin(radianDist) * np.cos(fromLat),
                      np.cos(radianDist) - np.sin(fromLat) * np.sin(fromLat))
    toLon = zero22pi(fromLon - dlon + np.pi) - np.pi
    return np.degrees(toLat), np.degrees(toLon)

def LatLonFrom(fromLat, fromLon, dist, azi, radius=6367470.0) :
    """
    Input and output longitudes and latitudes are in DEGREES.

    RETURNS (toLat, toLon)

    Uses the Vincenty's method, but assumes a perfect sphere in order to
    be usable as an inverse of GreatCircleDist() and Bearing()

    .. note ::
        The default value here has very little basis in accepted literature.
        When originally writing this function in C++, I merely took the
        straight average between the equatorial radius and the polar radius.
        A more valid value might be Q_r = 6372797.0 (equivalent great-circle
        radius of an Earth ellipsoid). However, I fear that changing this now
        might impact existing programs. Further investigations shall be done.
    """

    fromLat = np.radians(fromLat)
    fromLon = np.radians(fromLon)
    azi = np.radians(azi)

    """
    # Full Vincenty Method
    a = 6378137.0
    b = 6356752.3
    f = (a - b) / b
    t_U1 = (1 - f) * np.tan(fromLat)
    U_1 = np.arctan(t_U1)
    sigma_1 = np.arctan2(t_U1, np.cos(azi))
    alpha = np.arcsin(np.cos(U_1) * np.sin(azi))
    u_sqr = (np.cos(alpha)**2) * (a**2 - b**2) / b**2
    A = 1 + ((u_sqr / 16384) *
             (4096 + u_sqr *
              (-768 + u_sqr *
               (320 - 175 * u_sqr))))
    B = (u_sqr / 1024) * (256 + u_sqr *
                          (-128 + u_sqr *
                           (74 - 47 * u_sqr)))

    # Initial Guess
    delta_sigma = 0.0
    for i in xrange(20) :
        print np.mean(delta_sigma)
        sigma = dist / (b * A) + delta_sigma
        sigma_m_2 = 2 * sigma_1 + sigma
        delta_sigma = B * np.sin(sigma) * \
                      (np.cos(sigma_m_2) + 0.25 * B *
                       (np.cos(sigma) *
                        (-1 + 2 * np.cos(sigma_m_2)**2) -
                        0.166666 * B * np.cos(sigma_m_2) *
                        (-3 + 4 * np.sin(sigma)**2) *
                        (-3 + 4 * np.cos(sigma_m_2)**2)))
    sigma = dist / (b * A) + delta_sigma
    sigma_m_2 = 2 * sigma_1 + sigma

    toLat = np.arctan2(np.sin(U_1) * np.cos(sigma) +
                       np.cos(U_1) * np.sin(sigma) * np.cos(azi),
                       np.sqrt(np.sin(alpha)**2 +
                               (np.sin(U_1) * np.sin(sigma) -
                                np.cos(U_1) * np.cos(sigma) * np.cos(azi))**2) *
                       (1 - f))

    lmbda = np.arctan2(np.sin(sigma) * np.sin(azi),
                       np.cos(U_1) * np.cos(sigma) -
                       np.sin(U_1) * np.sin(sigma) * np.cos(azi))
    C = (f / 16) * np.cos(alpha)**2 * (4 + f * (4 - 3 * np.cos(alpha)**2))
    L = lmbda - (1 - C) * f * np.sin(alpha) *\
                (sigma + C * np.sin(sigma) *
                 (np.cos(sigma_m_2) + C * np.cos(sigma) *
                  (-1 + 2 * np.cos(sigma_m_2)**2)))
    """
    # Modified version of Vincenty's formula with the intention to minimize
    # differences between LonLat2Cart(Cart2LonLat()) and
    # Cart2LonLat(LonLat2Cart()) rather than being absolutely accurate in
    # one, but not the other.
    # Because LonLat2Cart() assumes a perfect sphere using GreatCircleDist(),
    # This function will do the same.

    # Assume perfect sphere  -- f = 0.0, a == b
    alpha = np.arcsin(np.cos(fromLat) * np.sin(azi))

    sigma = dist / radius
    toLat = np.arctan2(np.sin(fromLat) * np.cos(sigma) +
                       np.cos(fromLat) * np.sin(sigma) * np.cos(azi),
                       np.sqrt(np.sin(alpha)**2 +
                               (np.sin(fromLat) * np.sin(sigma) -
                                np.cos(fromLat) * np.cos(sigma) *
                                np.cos(azi))**2))

    #toLat = np.arcsin(np.sin(fromLat) * np.cos(sigma) +
    #                  np.cos(fromLat) * np.sin(sigma) * np.cos(azi))
    lmbda = np.arctan2(np.sin(sigma) * np.sin(azi),
                       np.cos(fromLat) * np.cos(sigma) -
                       np.sin(fromLat) * np.sin(sigma) * np.cos(azi))

    toLon = zero22pi(fromLon + lmbda + np.pi) - np.pi

    return (np.degrees(toLat), np.degrees(toLon))

def LonLat2Cart(st_lon, st_lat, lons, lats) :
    """
    Return the cartesian coordinates in km relative to
    *st_lon* and *st_lat*.

    .. seealso ::
        :func:`Cart2LonLat`     -- Inverse of LonLat2Cart()
    """
    dists = GreatCircleDist(st_lon, st_lat, lons, lats)
    bearings = Bearing(st_lon, st_lat, lons, lats)
    xs = dists * np.sin(bearings) / 1000.0
    ys = dists * np.cos(bearings) / 1000.0

    return xs, ys

def Cart2LonLat(st_lon, st_lat, xs, ys) :
    """
    Return the longitude/latitude coordinates in degrees relative to
    *st_lon* and *st_lat*.

    *xs* and *ys* are cartesian coordinates in km.

    .. seealso ::
        :func:`LonLat2Cart`     -- Inverse of Cart2LonLat()
    """
    # Yes, it is intentionally backwards because I want the angle
    # with 0 degrees pointing north and increasing clock-wise
    azimuth = np.arctan2(xs, ys)
    gates = np.hypot(xs, ys)

    lats, lons = LatLonFrom(st_lat, st_lon,
                            gates * 1000.0, np.degrees(azimuth))
    return lons, lats

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




