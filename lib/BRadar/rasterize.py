import numpy as np
from maputils import sph2latlon, latlon2pix, makerefmat


def Rastify(statLat, statLon, origData, azimuths, 
            rangeGates, elevAngle, deltaAz, deltaR, cellSize) :
    """
    RASTIFY    Covert data in spherical domain into rectilinear lat/lon domain

    Rastify(...) takes the vector or matrix of data points and places the
    points into a 2-D matrix organized by latitudes and longitudes.  The
    original data has a parallel vector or matrix of azimuths (in degrees North)
    and rangeGates (in meters) as well as a scalar elevAngle (in degrees).
    The origin of the spherical coordinates is given by the statLat (in
    degrees North) and statLon (in degrees East).  deltaAz denotes the 
    width of the beam in degrees while the deltaR scalar denotes the width 
    the of range gate in meters.

    The user specifies the resolution (in degrees) of the final product
    using cellSize.

    Author: Benjamin Root
    """
    goodValsInds = ~np.isnan(origData).flatten()
    origData = origData.flatten().compress(goodValsInds)
    azimuths = azimuths.flatten().compress(goodValsInds)
    rangeGates = rangeGates.flatten().compress(goodValsInds)
 
    # These arrays are for creating the verticies of the resolution volume
    # in 2-D.
    deltaAzMult = np.array([-1, -1, 1, 1])
    deltaRMult = np.array([-1, 1, 1, -1])
    
    # Getting the lat/lon locations of all the verticies.
    (tmpLat, tmpLon) = sph2latlon(statLat, statLon, 
				  azimuths[:, np.newaxis] + (deltaAzMult[np.newaxis, :] * deltaAz),
                  rangeGates[:, np.newaxis] + (deltaRMult[np.newaxis, :] * deltaR), 
				  elevAngle)
    
    # Automatically determine the domain,
    # note that this isn't friendly to crossing the prime-meridian.
    latlim = (tmpLat.min(), tmpLat.max())
    lonlim = (tmpLon.min(), tmpLon.max())
    latAxis = np.arange(latlim[0], latlim[1] + cellSize, cellSize)
    lonAxis = np.arange(lonlim[0], lonlim[1] + cellSize, cellSize)
    
    # Automatically determine the grid size from the calculated axes.
    gridSize = (len(latAxis), len(lonAxis))
    
    # Reference matrix is used to perform the 'affine' transformation from
    # lat/lon to the x-y coordinates that we need.
    # This can be adjusted later to allow for the user to specify a
    # different resolution for x direction from the resolution in the y
    # direction.
    R = makerefmat(lonlim[0], latlim[0], cellSize, cellSize)
    
    # Getting the x and y locations for each and every verticies.
    (tmpy, tmpx) = latlon2pix(R, tmpLat, tmpLon)
    
    # I wonder if it is computationally significant to get the min/max's of
    # each polygon's coordinates in one shot.  What about storage
    # requirements?
    
    # Initializing the data matrix.
    rastData = np.empty(gridSize)
    rastData[:] = np.nan
    
    for index in xrange(0, len(origData)) :
        resVol = zip(tmpx[index, [0, 1, 2, 3, 0]],
                     tmpy[index, [0, 1, 2, 3, 0]])


        # Getting all of the points that the polygon has, and then some.
        # This meshed grid is bounded by the domain.
        (ygrid, xgrid) = np.meshgrid(range(max(np.floor(min(tmpy[index, :])), 0),
                                           min(np.ceil(max(tmpy[index, :]) + 1), gridSize[0]),
                                           1),
        				range(max(np.floor(min(tmpx[index, :])), 0),
					          min(np.ceil(max(tmpx[index, :]) + 1), gridSize[1]),
                              1))                              
        gridPoints = zip(xgrid.flat, ygrid.flat)

        # Determines which points fall within the resolution volume.  These
        # points will be the ones that will be assigned the value of the
        # original data point that the resolution volume represents.
        goodPoints = point_inside_polygon(gridPoints, resVol)
	

	    # Assign values to the appropriate locations (the grid points that
        # were inside the polygon), given that the data value that might
        # already be there is less-than the value to-be-assigned, or if
        # there hasn't been a data-value assigned yet (NAN).
        # This method corresponds with the method used by NEXRAD.
        for containedPoint in zip(ygrid.flat[goodPoints], xgrid.flat[goodPoints]) :
            if (np.isnan(rastData[containedPoint])
                or (rastData[containedPoint] < origData[index])) :
                rastData[containedPoint] = origData[index]

    return (rastData, latAxis, lonAxis)


def point_inside_polygon(pnts, poly):
    n = len(poly)
    pnts = np.asanyarray(pnts)
    inside = np.zeros(pnts.shape[0], dtype=bool)

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]

        locs = ((pnts[:, 1] > min(p1y,p2y)) &
                (pnts[:, 1] <= max(p1y, p2y)) &
                (pnts[:, 0] <= max(p1x, p2x)) &
                ((p1x == p2x) | (pnts[:, 0] <= ((pnts[:, 1] - p1y)*(p2x-p1x)/(p2y-p1y)+p1x))))
        inside[locs] = ~inside[locs]
        p1x,p1y = p2x,p2y
    return inside

